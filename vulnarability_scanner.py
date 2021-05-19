#!/usr/bin/env python
import scanner
target_url = "http://testphp.vulnweb.com"
links_to_ignore = ["http://testphp.vulnweb.com/logout.php"]
data_dict = {"uname" : "test" , "pass" : "test"}
vuln_scanner = scanner.Scanner(target_url, links_to_ignore)
vuln_scanner.session.post("http://testphp.vulnweb.com/login.php" , data=data_dict)
vuln_scanner.crawl()
vuln_scanner.run_scanner()


