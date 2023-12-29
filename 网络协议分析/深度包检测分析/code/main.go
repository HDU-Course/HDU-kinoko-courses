package main

import (
	"log"
	"time"

	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/plotutil"
	"gonum.org/v1/plot/vg"
)

const (
	LowLatency         = "LowLatency"         // 低延迟
	GuaranteedLatency  = "GuaranteedLatency"  // 保证延迟
	GuaranteedDelivery = "GuaranteedDelivery" // 保证交付
	BestEffortDelivery = "BestEffortDelivery" // 尽力交付
)

type ServiceStats struct {
	HostCount    int     // 主机数量
	PacketRatio  float64 // 数据包比例
	AverageSpeed float64 // 平均速度
}

type ServiceTypeStats struct {
	ServiceType string        // 服务类型
	Stats       *ServiceStats // 服务统计信息
}

// 获取数据包的服务类型
func getServiceType(packet gopacket.Packet) string {
	// 检查是否为TCP数据包
	if tcpLayer := packet.Layer(layers.LayerTypeTCP); tcpLayer != nil {
		tcp, _ := tcpLayer.(*layers.TCP)
		// 检查TCP端口是否为22（SSH）
		if tcp.SrcPort == layers.TCPPort(22) || tcp.DstPort == layers.TCPPort(22) {
			return BestEffortDelivery
		}
		// 检查TCP端口是否为80（HTTP）、443（HTTPS）
		if tcp.SrcPort == layers.TCPPort(80) || tcp.DstPort == layers.TCPPort(80) || tcp.SrcPort == layers.TCPPort(443) || tcp.DstPort == layers.TCPPort(443) {
			return GuaranteedLatency
		}
		return GuaranteedDelivery
	}

	// 检查是否为UDP数据包
	if udpLayer := packet.Layer(layers.LayerTypeUDP); udpLayer != nil {
		udp, _ := udpLayer.(*layers.UDP)
		// 检查UDP端口是否为5060、5061（SIP）
		if udp.SrcPort == layers.UDPPort(5060) || udp.DstPort == layers.UDPPort(5060) || udp.SrcPort == layers.UDPPort(5061) || udp.DstPort == layers.UDPPort(5061) {
			return LowLatency
		}
		return GuaranteedDelivery
	}

	return GuaranteedDelivery
}

// 更新服务统计信息
func updateServiceStats(stats map[string]*ServiceStats, packet gopacket.Packet, serviceType string) {
	// 检查服务类型是否存在于统计信息中，如果不存在则创建一个新的统计信息
	if _, ok := stats[serviceType]; !ok {
		stats[serviceType] = &ServiceStats{}
	}
	length := packet.Metadata().CaptureLength
	hosts := make(map[string]bool)
	// 获取IPv4层的源IP和目标IP，并将其添加到hosts映射中
	if ipLayer := packet.Layer(layers.LayerTypeIPv4); ipLayer != nil {
		ip, _ := ipLayer.(*layers.IPv4)
		hosts[ip.SrcIP.String()] = true
		hosts[ip.DstIP.String()] = true
	}
	// 更新统计信息中的主机数量和数据包比例
	stats[serviceType].HostCount += len(hosts)
	stats[serviceType].PacketRatio += float64(length)
	packets := []struct {
		Length    int
		Timestamp time.Time
	}{
		{
			Length:    length,
			Timestamp: packet.Metadata().Timestamp,
		},
	}
	// 计算平均速度并更新统计信息中的平均速度
	stats[serviceType].AverageSpeed = calcAvgSpeed(packets)
}

// 计算平均速度
func calcAvgSpeed(packets []struct {
	Length    int
	Timestamp time.Time
}) float64 {
	// 如果数据包数量小于2，则返回0.0
	if len(packets) < 2 {
		return 0.0
	}
	firstPacketTime := packets[0].Timestamp
	lastPacketTime := packets[len(packets)-1].Timestamp
	totalBytes := 0
	// 计算所有数据包的总字节数
	for _, packet := range packets {
		totalBytes += packet.Length
	}
	// 计算时间间隔（秒）
	elapsedTime := lastPacketTime.Sub(firstPacketTime).Seconds()
	// 计算平均速度（字节/秒）
	return float64(totalBytes) / elapsedTime
}

// 绘制服务统计图表
func plotServiceStats(serviceStats []*ServiceTypeStats) {
	p := plot.New()
	p.Title.Text = "服务统计信息"
	p.X.Label.Text = "服务类型"
	p.Y.Label.Text = "值"

	serviceTypes := make([]string, len(serviceStats))
	hostCounts := make(plotter.Values, len(serviceStats))
	packetRatios := make(plotter.Values, len(serviceStats))
	averageSpeeds := make(plotter.Values, len(serviceStats))

	// 从服务统计信息中提取数据
	for i, stat := range serviceStats {
		serviceTypes[i] = stat.ServiceType
		hostCounts[i] = float64(stat.Stats.HostCount)
		packetRatios[i] = stat.Stats.PacketRatio
		averageSpeeds[i] = stat.Stats.AverageSpeed
	}

	// 创建柱状图
	hostCountBar, err := plotter.NewBarChart(hostCounts, vg.Points(20))
	if err != nil {
		log.Fatal(err)
	}
	hostCountBar.LineStyle.Width = vg.Length(0)
	hostCountBar.Color = plotutil.Color(0)
	hostCountBar.Offset = -vg.Points(10)

	packetRatioBar, err := plotter.NewBarChart(packetRatios, vg.Points(20))
	if err != nil {
		log.Fatal(err)
	}
	packetRatioBar.LineStyle.Width = vg.Length(0)
	packetRatioBar.Color = plotutil.Color(1)

	averageSpeedBar, err := plotter.NewBarChart(averageSpeeds, vg.Points(20))
	if err != nil {
		log.Fatal(err)
	}
	averageSpeedBar.LineStyle.Width = vg.Length(0)
	averageSpeedBar.Color = plotutil.Color(2)
	averageSpeedBar.Offset = vg.Points(10)

	// 将柱状图添加到图表中并设置图例
	p.Add(hostCountBar, packetRatioBar, averageSpeedBar)
	p.Legend.Add("主机数量", hostCountBar)
	p.Legend.Add("数据包比例", packetRatioBar)
	p.Legend.Add("平均速度", averageSpeedBar)
	p.NominalX(serviceTypes...)

	// 保存图表为PNG图片
	if err := p.Save(6*vg.Inch, 4*vg.Inch, "service_stats.png"); err != nil {
		log.Fatal(err)
	}
}

func main() {
	handle, err := pcap.OpenOffline("package.pcap")
	if err != nil {
		log.Fatal(err)
	}
	defer handle.Close()

	// 创建数据包源，使用与处理句柄相同的链路类型
	packetSource := gopacket.NewPacketSource(handle, handle.LinkType())

	serviceStats := make(map[string]*ServiceStats)

	totalPackets := 0

	for packet := range packetSource.Packets() {
		totalPackets++

		serviceType := getServiceType(packet)

		updateServiceStats(serviceStats, packet, serviceType)

		if totalPackets == 7200 {
			break
		}
	}

	// 归一化处理服务统计信息
	for _, stat := range serviceStats {
		stat.PacketRatio = stat.PacketRatio / float64(totalPackets)
	}

	// 将服务统计信息映射表转换为切片类型
	convertedServiceStats := make([]*ServiceTypeStats, 0, len(serviceStats))
	for serviceType, stats := range serviceStats {
		convertedServiceStats = append(convertedServiceStats, &ServiceTypeStats{
			ServiceType: serviceType,
			Stats:       stats,
		})
	}

	// 绘制服务统计图表并保存为文件
	plotServiceStats(convertedServiceStats)
}
