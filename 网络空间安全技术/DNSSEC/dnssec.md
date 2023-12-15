# DNSSEC
本篇文章发布在阿菇的[个人博客](https://ma5hr00m.top)，可以直接用作DNSSEC Topic讲解的文案。

## 脆弱的DNS

DNS（Domain Name System）是一种用于将易于理解的域名转换为计算机可读的IP地址的系统。
从其功能来说，它就像互联网中的“电话簿”，通过管理域名和IP地址之间的映射关系，使得计算机和其他网络设备能够相互通信。

举个例子：用户在浏览器中访问一个域名，比如`ma5hr00m.top`，需要先知道这个域名对应的IP地址，计算机通过DNS查询到域名对应的IP地址是`101.35.240.239`，它就会与这个IP对应的机器通信。

更详细地说“通过DNS查询到域名对应的IP”这个过程：DNS系统由多个层级的域名服务器组成，这些服务器相互协作来处理DNS查询。当用户在浏览器中输入域名并请求访问网站时，操作系统会向*本地DNS解析器*发出查询请求。如果本地解析器缓存了相应的IP地址，它会直接返回结果；否则，它会向互联网上的*根域名服务器*发出请求。根域名服务器会指导本地解析器到达*顶级域名服务器*，然后再到达*次级域名服务器*，直到找到负责特定域名的*权威域名服务器*。最终，权威域名服务器会返回所请求域名对应的IP地址，使得用户的设备能够连接到相应的服务器。

该流程可以总结成这张图，更好理解：

![20231208062310](https://img.ma5hr00m.top/blog/20231208062310.png)

现在我们知道什么是DNS了，那我们为什么需要DNS？因为直接记忆IP地址比较麻烦（尤其是IPV6出现之后），而有意义的字符串更方便记忆。`20.205.243.166`和`github.com`，我们愿意记哪一个呢？

> 使用`nslookup xxx.xxx`指令来查询域名对应的IP地址。
> 
> 该工具包含在`dnsutils`（Debian/Arch）和`bind-utils`（CentOS/RHEL）中。

DNS最早在1983年的[RFC 882](https://datatracker.ietf.org/doc/html/rfc882)中定义，并提供了技术实现，现今已成为互联网的基础设施之一。但经过多年发展，互联网环境日趋复杂，远不像那个时代那般“单纯”，DNS的脆弱就体现出来了。

理由无他，DNS在设计之初就没有提供任何安全措施：基于UDP的明文数据传输、无身份验证、无数据完整性验证……如果我们仅使用传统的DNS协议，这无异于只穿条裤衩就上街。对于有心者，我们的数据一览无遗。

后世的人们自然也发现了这个问题，毕竟谁都不想让自己的数据裸奔。然后就出现了很多种解决方案，比如为DNS服务器添加入侵检测系统、设置DNS过滤器、对应的加密协议`DNS on TLS`……这其中，就包括DNS安全拓展，也就是DNSSEC。

## 可靠的DNSSEC
DNSSEC（Domain Name System Security Extensions）是一种用于增强域名系统（DNS）安全性的协议扩展，也就是由 IETF 提供的一套DNS安全认证机制（可参考[RFC 2535](https://tools.ietf.org/html/rfc2535)）。它通过添加加密验证机制，防止DNS查询过程中的欺骗和篡改，确保用户访问的网站和服务器是合法和可信的。

## 相关概念
### 新的DNS记录类型
DNSSEC通过向现有DNS记录添加加密签名，确保域名系统的安全性，这些数字签名与`A、AAAA、MX、CNAME`等常见记录类型一起存储在DNS名称服务器中。计算机可以通过检查相关签名，去验证请求的DNS记录是否来自权威名称服务器，以及有没有被篡改过。

- RRSIG：包含加密签名
- DNSKEY：包含公共签名密钥
- DS：包含DNSKEY记录的Hash
- NSEC和NSEC3：用于明确否认DNS记录的存在
- CDNSKEY和CDS：用于请求对父区域中的DS记录进行更新的子区域。

先有个印象，下文细说，

### Resource Record Set
资源记录集，即RRSets。使用 DNSSEC 保护某个区域的第一步，是将所有相同类型的记录分组到一个RRSets中，也就是进行分组。

比如，example.com域下有三条AAAA类型的记录，分别为：

- `a.example.com 300 IN AAAA 2001:0db8:85a3:0000:0000:8a2e:0370:7334`
- `b.example.com 600 IN AAAA 2001:0db8:85a3:0000:0000:8a2e:0370:7335`
- `c.example.com 900 IN AAAA 2001:0db8:85a3:0000:0000:8a2e:0370:7336`

<div align="center">
  <img style="width:100%;" src="https://img.ma5hr00m.top/blog/20231208073028.png" alt="KSK&ZSK">
</div>

我们可以将其捆绑到同一组中，这就是一个RRset。

### Zone-Singing Key
区域签名密钥，即ZSK。

DNSSEC中的每个区域都有一个ZSK。ZSK通常是RSA密钥对，包括公钥（公用）和私钥（专用）两部分，其中专用部分对区域中的每个RRset进行数字签名，而公共部分则验证签名。

为了启用DNSSEC，区域操作员需要使用ZSK专用部分为每个RRset创建数字签名，并将其作为`RRSIG`记录存储在名称服务器中，并将公用共用部分添加到`DNSKEY`记录中的名称服务器，使其可用。

当DNSSEC解析器请求特定的记录类型（例如 AAAA）时，名称服务器就返回相应的`RRSIG`。然后，解析器可以从名称服务器中提取包含ZSK共用部分的`DNSKEY`记录。就这样，RRset、RRSIG和公共ZSK将一同用于验证响应。

### Key-Singing Key
密钥签名密钥，即KSK。

KSK验证`DNSKEY`记录的方式与上文ZSK保护RRset的方式相同：
使用KSK的私钥签署ZSK公钥（存储在 DNSKEY 记录中），并为其`DNSKEY`创建`RRSIG`；然后，计算机将KSK放入DNSKEY记录中。

就像公共ZSK一样，名称服务器将公共KSK发布在另一个`DNSKEY`记录中，而这就给计算机提供了上面显示的`DNSKEY`RRset。
公共KSK和公共ZSK均由私有KSK签名。然后，解析器就可以使用公共KSK来验证公共ZSK。

<div align="center">
  <img style="width:100%;" src="https://img.ma5hr00m.top/blog/20231208115854.png" alt="KSK&ZSK">
</div>

简单地说，KSK就是用于保护密钥的密钥。
ZSK负责保护RRset的安全，KSK负责保护ZSK的安全。
而KSK的主要作用是建立信任链，将父区域的信任传递给子区域。

### Delegation Signer
委派签名者，即DS。

DNSSEC引入了DS记录，用于在父区域和子区域之间建立*信任链*。区域操作员将子区域的公共KSK的Hash作为DS记录发布到父区域。当解析器引用子区域时，父区域提供DS记录，解析器通过比较子区域公共KSK的哈希值和父区域的DS记录来验证公共KSK的有效性。如果匹配成功，解析器就可以信任子区域的所有记录。

<div align="center">
  <img style="width:100%;" src="https://img.ma5hr00m.top/blog/20231208123822.png" alt="KSK&ZSK">
</div>

### 信任链
这一套操作下来，我们使用RRset+ZSK+KSK的认证机制保证了区域内的安全，又通过DS保证了子区域到父区域的安全。那问题来了：我们应该如何信任DS记录呢，换句话说，我们该如何得知父区域是否安全可信？

那自然是去找父区域的父区域啦～

DS记录本身就像其他任何RRset一样签署，这意味着它在父级中也具有相应的RRSIG。我们所要做的就是不断重复上面的过程，区域内的ZSK+KSK验证做完就去找父区域的公共KSK，父区域的KSK+ZSK验证完成就继续往上找……这样的验证方式就会自底而上形成一条链子，称为*信任链*。

链子总归是有个头的。我们向链子的根源不断摸索，最后看到的是——

![DNSSEC根签名仪式](https://www.cloudflare.com/img/products/official-ceremony-photo.jpg)

> 这张图是根域签名仪式人员在ICANN的合影。

### 根域签名仪式
像前文所说，我们不断重复验证，最终来到信任链的终点（或者说起点）——*根DNS区域*。那现在问题来了：根区域没有父区域。我们可以在根DNS区域获取一个`RRSIG`记录，通过这个记录验证根名称服务器的公共KSK和ZSK。但我们没有所需的DS来验证这个`RRSIG`记录的安全性。

怎么办呢？
即使是聪明的大脑也没有合适的解决方法，所以，我们采取了朴实无华的方法……

每隔一段时间，相关负责机构会召集一群人，以公开且经严格审核的方式签署*根DNSKEY RRset*，继而产生一条`RRSIG`记录用于验证根名称服务器的公共KSK和ZSK。也就是说，根区域的公共KSK是没有DS记录来保证安全性的，我们只是假定它足够安全有效。

当然啦，事实上也足够安全。我无意去介绍这个仪式的流程，总之就是十分的严谨繁琐冗长——都是为了互联网的安全。仪式最后得到的就是那条`RSSIG`数据。

> 前面说到过，整个仪式的过程是公开的，这个[视频](https://www.youtube.com/watch?v=EOb0Zu3hy2U)是距本篇博客写作最近的一次根域签名仪式录播，长达4.5h。
> 
> 这篇[文章](https://www.cloudflare.com/zh-cn/dns/dnssec/root-signing-ceremony/)则是对根域签名仪式全过程的记述。

### 为什么需要KSK
DNS是一个分层系统，各区域很少独立运行。
像上文说的DS记录，就是为了将父区域的信任传递给子区域，DS记录本身就是公共KSK的Hash。
只要更换KSK就需要更改父区域的DS记录。
而更改DS记录是一个多步骤的过程，如果执行不正确，最终可能会破坏该区域。

这意味着，更换KSK的成本很高。如果我们把ZSK和KSK合二为一，使其既承担信任传递功能又承担加密RRset功能，那我们每次想要对子区域内密钥进行更换都会变得繁琐。而更换ZSK只需要在特定区域内进行操作，不会涉及到父区域的DS记录的修改。将二者独立开来，就可以在保证信任链的前提下，提供更好的灵活性，使区域操作员更容易更换ZSK，以保证RRset的安全。

> KSK用于建立信任链，确保子区域的公钥的有效性；而ZSK用于签名特定区域的数据，保证数据的完整性和身份验证。d

## 完整流程
前面讲得比较零散，可能你仍不清楚一次`DNS with DNSSEC`查询到底要怎么将以上所有点结合起来。我下面以`ma5hr00m.top`为例，走一遍完整的流程：

1. 解析器向根域名服务器发送查询请求，询问顶级域名服务器(.域)的NS记录。
2. 根域名服务器回复解析器，提供顶级域名服务器(.域)的NS记录。
3. 解析器向顶级域名服务器(.域)发送查询请求，询问`.ma5hr00m.top`域的NS记录。
4. 顶级域名服务器(.域)回复解析器，提供`ma5hr00m.top`域的NS记录。
5. 解析器向`ma5hr00m.top`域的权威域名服务器发送查询请求，询问`ma5hr00m.top`域的A记录。
6. 权威域名服务器回复解析器，提供`ma5hr00m.top`域的A记录为`101.35.240.239`。
7. 解析器同时获取到`ma5hr00m.top`域的A记录的`RRSet`的签名`RRSIG`，并使用该签名的`ZSK`进行验证，确保数据的完整性和身份验证。
8. 解析器向`ma5hr00m.top`域的权威域名服务器发送查询请求，询问`ma5hr00m.top`域的`DNSKEY`记录。
9. 权威域名服务器回复解析器，提供`ma5hr00m.top`域的`ZSK`和`KSK`公钥，并同时提供`DNSKEY RRSet`的签名`RRSIG`。
10. 解析器使用获取到的`KSK`验证上一步得到的`DNSKEY`记录，确保数据的完整性和身份验证。
11. 解析器使用获取到的`ZSK`验证第五步得到的A记录，确保数据的完整性和身份验证。
12. 为了保证`DNSKEY RRSIG`中的KSK不被伪造，解析器请求`.ma5hr00m.top`域与`ma5hr00m.top`相关的DS记录，并获取到DS记录的`RRSIG`。
13. 解析器计算`KSK`的哈希值，并使用获取到的DS记录的`RRSIG`进行验证，确保数据的完整性和身份验证。
14. 解析器重复步骤12和步骤13，向顶级域名服务器(.域)请求`.ma5hr00m.top`域的DS记录，并获取到DS记录的`RRSIG`。
15. 解析器重复步骤12和步骤13，向根域名服务器请求`.ma5hr00m.top`域的DS记录，并获取到DS记录的`RRSIG`。
16. 解析器使用根域名服务器提供的DS记录的`RRSIG`进行验证，确保数据的完整性和身份验证。
17. 验证通过后，解析器将最终的结果`101.35.240.239`返回给用户。

然后，我们就安全地获取到了`ma5hr00m.top`对应的IP地址：`101.35.240.239`！

## DNSSEC的优劣
原理讲完了，说说为什么要使用DNSSEC。

作为一个安全拓展，使用DNSSEC最重要的好处就是保护DNS提供的数据，确保互联网上的路标（DNS记录）指向正确的内容或服务，以防止攻击者篡改DNS数据，导致用户被引导到错误的网站或不安全的地方。从根本上来讲，就是保护用户的安全。具体点说，就是可以在一定程度上防止DNS投毒、DNS劫持、DNS重放等攻击手段。

数据变得可信之后，相继地，这份可信的数据也会促进全球DNS的应用。我们利用这些数据创建了一个*安全的域名/值数据库*，这个安全的数据库可以提供多种创新机会，支持新的技术、服务和设施。互联网研究人员就可以利用这些“干净”的数据来做一些有趣的实验，研发一些新技术。比如DANE（DNS-based Authentication of Named Entitie）就是在利用DNS中受DNSSEC保护的数据，期望解决当前互联网安全连接方法中存在的一些漏洞。

此外呢，从广义上来讲，DNS 涉及两个方面：发布，由注册人或其代理执行；以及解析，通常由网络运营商（例如，互联网服务提供商）来完成。
也就是说，使用DNSSEC需要两端同时发力。

而DNSSEC很早就大规模部署了。所有根域名服务器在2010年就部署了DNSSEC，若干顶级域名（`.org`、`.com`、`.net`和`.edu`等）服务器也在2011年部署了DNSSEC。
相比其他DNS保护措施，DNSSEC的普及度可以说是遥遥领先了，多数公共的域名服务器都支持它。

> 查询DNSSEC支持情况：[Notable public DNS servicde operators](https://en.wikipedia.org/wiki/Public_recursive_name_server#Notable_public_DNS_service_operators)

DNSSEC也是最早大规模部署的。在 2010 年的时候，所有根域名服务器都已经部署了 DNSSEC。到了 2011 年，若干顶级域名（.org 和 .com 和 .net 和 .edu）也部署了 DNSSEC。

但是，DNSSEC也并不完美。DNSSEC仅仅是对传输的数据做了数字签名，但未进行加密。如果你的网络流量被别人监视，他依然可以得知你在访问什么域名。可是是出于这个原因，Chrome曾支持过DNSSEC但随后移除，Firefox则从未支持过DNSSEC。

另外，DNSSEC的使用显著增加了DNS查询响应的数量（需要额外的字段和加密信息来正确验证记录），这就增加了计算机增加遭受分布式拒绝服务 (DDoS) 攻击的风险。

## 后话
可能是出于对部署DNSSEC收益的考量，DNS出现于1980年，相关安全问题在08-11年大规模爆发，直到2013年，DNSSEC才开始快速普及。截至2021年，尽管DNSSEC解析服务器只占总量的 17.4%，但其请求量已经超过七成。按照国家来看，平均使用率为14%，而中国的DNSSEC使用率仅6%左右。

## 参考 
- [什么是 DNS | DNS 的工作方式](https://www.cloudflare.com/zh-cn/learning/dns/what-is-dns/)，by CloudFlare
- [DNSSEC 如何运作](https://www.cloudflare.com/zh-cn/dns/dnssec/how-dnssec-works/)，by CloudFlare
- [4种DNS安全协议对比](https://www.wosign.com/News/news_2019032201.htm)，by WoTrust
- [重启DNS根密钥服务器的七个人](https://www.cernet.com/hlwjsyj/202009/4606.html)，by 赛尔网络
- [DNSSEC：保护DNS的安全](https://www.icann.org/zh/system/files/files/octo-006-24jul20-zh.pdf)，by ICANN首席技术官办公室
- [对比4种强化域名安全的协议](https://herbertgao.com/15/#DNSSEC)，by HerbertGao0
- [DNSSEC的选择：Yes还是No？](https://www.edu.cn/xxh/zt/tj/202305/t20230518_2408472.shtml)，by 中国教育网络 