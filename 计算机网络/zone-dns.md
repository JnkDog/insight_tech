## zone file
```cfg
; IPv4 zone file for example.com
$TTL 2d ; default TTL for zone
$ORIGIN example.com.   ; 给这个域名提供服务
; Start of Authority record defining the key characteristics of the zone (domain)
@ IN SOA ns1.example.com. hostmaster.example.com. (
    2003080800 ; sn = serial number
    12h ; refresh
    15m ; retry = update retry
    3w ; expiry
    2h ; min = minimum
)
; name servers Resource Records for the domain
    IN NS ns1.example.com.    ;一个域名解析服务
; the second name servers is
; external to this zone (domain).
    IN NS ns2.example.net.    ;另一个？？地址呢？
; mail server Resource Records for the zone (domain)
    3w IN MX 10 mail.example.com.
; the second mail servers is
; external to the zone (domain)
    IN MX 20 mail.anotherdomain.com.
; domain hosts includes NS and MX records defined above
; plus any others required
ns1    IN A 192.168.254.2
mail   IN A 192.168.254.4
joe    IN A 192.168.254.6
www    IN A 192.168.254.7
```