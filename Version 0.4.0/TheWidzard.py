import nmap
import aiohttp
import asyncio
import socket
from aiohttp import ClientTimeout

# Facade strucuture for TheWidzard

class Reconnaissance_Tool():

    ######################################
    #PORT SCANNER BLOCK: (aiohttp and nmap):

    #basic port scanning:
    async def _port_scanner(self, ip, port):


        try:
            connection_port_scanner = asyncio.open_connection(ip, port) #Attempt of connection to port "port"
            reader, writer = await asyncio.wait_for(connection_port_scanner, timeout=0.1) #Assignment of reader and writer variable (TCP connection channels)

            print(f"[PORT] {port} OPEN") # Successful attempt

            banner = await reader.read(1024) #Reading of the banner, if it's present, with a max size of 1024 bytes
            banner_decoded = banner.decode(errors="ignore") # Decoding of the banner, if it's present, ignoring errors
            if banner_decoded: # If the banner is not empty
                print(f"[BANNER] {port} {banner_decoded.strip()}") # Output of the banner
                self.banners.append(banner_decoded.strip()) # The banner must be added to the banners list
            writer.close() #Closing the writer channel
            await writer.wait_closed() #Wating until complete
            
        except asyncio.TimeoutError:
            pass  # Port scanning took too long
        except ConnectionRefusedError:
            print(f"[PORT] {port} access denied")  # Port scanning was denied
        except OSError:
            print(f"[PORT] {port} server unreachable")  #  Port scanning is impossible, server unreachable
    
    async def Port_Scanner(self, ip, ports=None): # Callable function
        self.banners = [] # for each ip there are new banners, the old ones must be removed
        if ports is None:
            ports = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]
        await asyncio.gather(*[self._port_scanner(ip, port) for port in ports]) # Attempting port scanning for each port

    #NMAP port scanning:

    async def Nmap_port_scanning(self, ip): #Advanced nmap tool
        nm = nmap.PortScanner()     #defining the instance
        nm.scan(ip, arguments="-sV -O") #nmap scanning, (ARGUMENTS: VERSION DETECTION AND REMOTE OS DETECTION)
        for port in nm[ip]["tcp"]:  #scanning the ip with known tcp ports known to nmap
            print(f"[OUTPUT-{port}] {nm[ip]['tcp'][port]['state']} - {nm[ip]['tcp'][port]['name']}") #output of state and name for each port

    ######################################
    #HTTP INFO REQUEST BLOCK:

    async def fetch_info(self, session, url):
        try:
            async with session.get(url, timeout=ClientTimeout(total=5)) as r:  # Http general get requests
                return r.status, await r.text()   # Returns status and text
        except aiohttp.ClientError as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
            return None, None
        except asyncio.TimeoutError:
            print(f"[ERROR] Timeout fetching {url}")
            return None, None


    ######################################
    #SUBDOMAIN SCANNER BLOCK:

    #This function is necessary, it inserts
    #the word into the url to search along all well-known subdomains


    def insert_word(self, url, word):   #The function takes the original url and the word to insert
        prec_i = ""      # The char that preceeds the analyzed one, it is initialized as an empty char

        for idx, i in enumerate(url): # This cycle searches along the url
        
            if i != "/" and prec_i == "/": # If i is positionated in the intended place 
        
                idx_insert = idx   # The index of the insertion is the observed one
                break  # Stop the cycle if it verificates the condition
        
            prec_i = i  # The previous i is the actual before it changes
        
        domain = url[idx_insert:]    # Definition of the domain part
        url = url[:idx_insert] + word + "." + domain # Rewriting of the url
        
        return url    # Returned value

    async def Subdomain_Scanner(self, session, url):  # This fuction is the one that'll be called by the Widzard
    # Asyncronized function
        # Awaited action that analyzes a list of words for an url
        await asyncio.gather(*[self._word_scan(session, url, word) for word in self.wordlist])
   
    async def _word_scan(self, session, url, word): # This function is not going to be called by TheWidzard
        # Target is the new url
        target = self.insert_word(url, word)
        
        # The new url is going to be analyzed by the get command
        try:
            async with session.get(target, timeout=ClientTimeout(total=3)) as r:
                print(f"[FOUND] {target} - status {r.status}")
        
        except aiohttp.ClientError:
            pass
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            print(f"[DEBUG] Unexpected error scanning {target}: {type(e).__name__}")

    ######################################

    def Recon_Spell(self):
        pass


class Vulnerability_Assesment_Tool():
    
    ######################################
    # HEADER ANALYZER BLOCK:

    async def Header_Analyzer(self, session, url):  #callable function for header analyzing
        try:
            async with session.get(url, timeout=ClientTimeout(total=5)) as r: #http get request
                for header in self.security_headers:  #for every header that is in the security_header list
                    if header in r.headers:  #if it's found
                        print(f"[FOUND]: {header}")
                    else: #if it's missing
                        print(f"[MISSING]: {header}")
        except aiohttp.ClientError as e:
            print(f"[ERROR] Failed to analyze headers for {url}: {e}")
        except asyncio.TimeoutError:
            print(f"[ERROR] Timeout analyzing headers for {url}")



    ######################################
    #CVE LOOKUP BLOCK:


    
    ######################################       
    
            
    def Vuln_Asses_Spell(self):
        pass

class Exploitation_tool():

    def Exploit_Spell(self):
        pass

class Post_Exploitation_tool():
    
    def Post_Exploit_Spell(self):
        pass

class Network_tool():
    
    def Network_Spell(self):
        pass


class OSINT_tool():

    def OSINT_Spell(self):
        pass

# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║  ████████╗██╗  ██╗███████╗    ██╗    ██╗██╗███████╗ █████╗ ██████╗ ██████╗    ║          
# ║     ██╔══╝██║  ██║██╔════╝    ██║    ██║██║╚══███╔╝██╔══██╗██╔══██╗██╔══██╗   ║         
# ║     ██║   ███████║█████╗      ██║ █╗ ██║██║  ███╔╝ ███████║██████╔╝██║  ██║   ║         
# ║     ██║   ██╔══██║██╔══╝      ██║███╗██║██║ ███╔╝  ██╔══██║██╔══██╗██║  ██║   ║         
# ║     ██║   ██║  ██║███████╗    ╚███╔███╔╝██║███████╗██║  ██║██║  ██║██████╔╝   ║         
# ║     ╚═╝   ╚═╝  ╚═╝╚══════╝     ╚══╝╚══╝ ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝    ║        
# ╚═══════════════════════════════════════════════════════════════════════════════╝

class TheWidzard(Reconnaissance_Tool, 
                Vulnerability_Assesment_Tool,
                Exploitation_tool, Post_Exploitation_tool,
                Network_tool, OSINT_tool):
    
    #List of subdomains to analyze:

    wordlist = ["mail", "api", "dev", "admin", "test", "staging", "vpn"] 

    #List of banners that have been taken: {DO NOT ADD ANY}

    banners = []

    #List of headers to analyze:
    
    security_headers = [
            "Strict-Transport-Security",
            "X-Frame-Options",
            "Content-Security-Policy",
            "X-Content-Type-Options",
    ]

        #List of links to check:
    urls = [
            "https://www.piaggiogroup.com",
            "https://www.amedei.it",
            "https://www.revet.com",
            "https://www.ecofor.it",
            "http://www.tmm.it",
            "https://www.assoworks.it",
            "https://www.castellani.it",
            "https://www.bianchirecyclix.it",
            "https://www.lapigroup.it",
            "https://www.modulblok.it"
    ]
        
    async def Cast_Spell(self): #Test function for the Widzard, it calls all the functions of the inherited classes
        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                print(f"\n{'='*50}")
                print(f"[TARGET] {url}")
                print(f"{'='*50}")

                print("\n[*] FETCH INFO")
                status, body = await self.fetch_info(session, url)
                if status:
                    print(f"[STATUS] {status}")
                    print(f"[BODY] {body[:100]}")

                print("\n[*] HEADER ANALYZER")
                await self.Header_Analyzer(session, url)

                print("\n[*] SUBDOMAIN SCANNER")
                await self.Subdomain_Scanner(session, url)

                print("\n[*] PORT SCANNER")
                domain = url.replace("https://", "").replace("http://", "").replace("www.", "")
                try:
                    ip = socket.gethostbyname(domain)
                    print(f"[RESOLVED] {domain} -> {ip}")
                    await self.Port_Scanner(ip)
                except socket.gaierror:
                    print(f"[ERROR] Could not resolve {domain}")
                                
                print("\n[*] CVE LOOKUP")


    @classmethod
    def add_word(cls):
        new_word = input(f"ADD A NEW WORD TO CHECK IN THE SUBDOMAIN SCANNER: ")
        cls.wordlist.append(new_word)

    @classmethod
    def add_header(cls):
        new_header = input(f"ADD A NEW HEADER TO CHECK IN THE HEADER ANALYZER: ")
        cls.security_headers.append(new_header)

    @classmethod

    def add_url(cls):
        new_url = input(f"ADD A NEW URL TO CHECK: ")
        cls.urls.append(new_url)



Witch = TheWidzard()

asyncio.run(Witch.Cast_Spell())