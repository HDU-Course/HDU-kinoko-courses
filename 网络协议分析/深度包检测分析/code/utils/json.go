package main

import (
	"encoding/json"
	"log"
	"os"
	"time"

	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
)

const (
	LowLatency         = "LowLatency"
	GuaranteedLatency  = "GuaranteedLatency"
	GuaranteedDelivery = "GuaranteedDelivery"
	BestEffortDelivery = "BestEffortDelivery"
)

type ServiceStats struct {
	HostCount    int     `json:"hostCount"`
	PacketRatio  float64 `json:"packetRatio"`
	AverageSpeed float64 `json:"averageSpeed"`
}

func getServiceType(packet gopacket.Packet) string {
	if tcpLayer := packet.Layer(layers.LayerTypeTCP); tcpLayer != nil {
		tcp, _ := tcpLayer.(*layers.TCP)
		if tcp.SrcPort == layers.TCPPort(22) || tcp.DstPort == layers.TCPPort(22) {
			return BestEffortDelivery
		}
		if tcp.SrcPort == layers.TCPPort(80) || tcp.DstPort == layers.TCPPort(80) || tcp.SrcPort == layers.TCPPort(443) || tcp.DstPort == layers.TCPPort(443) {
			return GuaranteedLatency
		}
		return GuaranteedDelivery
	}

	if udpLayer := packet.Layer(layers.LayerTypeUDP); udpLayer != nil {
		udp, _ := udpLayer.(*layers.UDP)
		if udp.SrcPort == layers.UDPPort(5060) || udp.DstPort == layers.UDPPort(5060) || udp.SrcPort == layers.UDPPort(5061) || udp.DstPort == layers.UDPPort(5061) {
			return LowLatency
		}
		return GuaranteedDelivery
	}

	return GuaranteedDelivery
}

func updateServiceStats(stats map[string]*ServiceStats, packet gopacket.Packet, serviceType string) {
	if _, ok := stats[serviceType]; !ok {
		stats[serviceType] = &ServiceStats{}
	}
	length := packet.Metadata().CaptureLength
	hosts := make(map[string]bool)
	if ipLayer := packet.Layer(layers.LayerTypeIPv4); ipLayer != nil {
		ip, _ := ipLayer.(*layers.IPv4)
		hosts[ip.SrcIP.String()] = true
		hosts[ip.DstIP.String()] = true
	}
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
	stats[serviceType].AverageSpeed = calcAvgSpeed(packets)
}

func calcAvgSpeed(packets []struct {
	Length    int
	Timestamp time.Time
}) float64 {
	if len(packets) < 2 {
		return 0.0
	}
	firstPacketTime := packets[0].Timestamp
	lastPacketTime := packets[len(packets)-1].Timestamp
	totalBytes := 0
	for _, packet := range packets {
		totalBytes += packet.Length
	}
	elapsedTime := lastPacketTime.Sub(firstPacketTime).Seconds()
	return float64(totalBytes) / elapsedTime
}

func main() {
	handle, err := pcap.OpenOffline("../package.pcap")
	if err != nil {
		log.Fatal(err)
	}
	defer handle.Close()

	packetSource := gopacket.NewPacketSource(handle, handle.LinkType())

	serviceStats := make(map[string]*ServiceStats)

	totalPackets := 0

	for packet := range packetSource.Packets() {
		totalPackets++
		serviceType := getServiceType(packet)
		updateServiceStats(serviceStats, packet, serviceType)
		if totalPackets == 3600 {
			break
		}
	}

	for _, stats := range serviceStats {
		stats.PacketRatio = stats.PacketRatio / float64(totalPackets)
	}

	// Convert serviceStats to JSON
	jsonData, err := json.MarshalIndent(serviceStats, "", "  ")
	if err != nil {
		log.Fatal(err)
	}

	// Save JSON data to a file
	err = saveJSONToFile(jsonData, "../service_stats.json")
	if err != nil {
		log.Fatal(err)
	}
}

func saveJSONToFile(jsonData []byte, filename string) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	_, err = file.Write(jsonData)
	if err != nil {
		return err
	}

	return nil
}
