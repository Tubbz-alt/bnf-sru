"""
Created on Thu May 31 09:30:13 2018

@author: BNF0017855
"""

import csv
from unidecode import unidecode
from lxml import etree
import http.client
from urllib import request
import urllib.parse
import urllib.error as error
from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
from nna_genres_formes import listeNNA_genres_formes
from listeISBN import listeISBN


ns = {"srw":"http://www.loc.gov/zing/srw/", "mxc":"info:lc/xmlns/marcxchange-v2", "m":"http://catalogue.bnf.fr/namespaces/InterXMarc","mn":"http://catalogue.bnf.fr/namespaces/motsnotices"}
nsClassify = {"classify":"http://classify.oclc.org"}
urlSRUroot = "http://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query="
sparql = SPARQLWrapper("http://data.bnf.fr/sparql")

#listeISBN = ["978-2-07-046410-4","978-2-07-078435-6","978-2-07-046469-2","978-2-07-046467-8","978-2-07-057875-7","978-2-07-078558-2","978-2-07-046713-6","978-2-07-046468-5","978-2-07-079351-8","978-2-07-077634-4","978-2-07-046885-0","978-2-07-079349-5","978-2-07-046923-9","978-2-07-079355-6","978-2-07-046749-5","978-2-07-046926-0","978-2-07-046492-0","978-2-07-046895-9","978-2-07-079353-2","978-2-07-079272-6","978-2-07-046826-3","978-2-07-079350-1","978-2-07-079346-4","978-2-07-077653-5","978-2-07-046825-6","978-2-07-046896-6","978-2-07-046823-2","978-2-07-046389-3","978-2-07-046390-9","978-2-07-046388-6","978-2-07-079363-1","978-2-07-046568-2","978-2-07-046830-0","978-2-07-046902-4","978-2-07-046900-0","978-2-07-046508-8","978-2-07--045815-8","978-2-07-046929-1","978-2-07-046482-1","978-207-046565-1","978-2-07-046205-6","978-2-07-079288-7","978-2-07-079324-2","978-2-07-046483-8","978-2-07-079321-1","978-2-07-046835-5","978-2-07-078513-1","978-2-07-046569-9","978-2-07-046839-3","978-2-07-046836-2","978-2-07-046927-7","978-2-07-046745-7","978-2-07-046623-8","978-2-07-268867-6","978-2-07-270420-8","978-2-07-270425-3","978-2-07-079220-7","978-2-07-077355-8","978-2-07-046195-0","978-2-07-270231-0","978-2-07-079336-5","978-2-07-056007-3","978-2-07-056006-6","978-2-07-057991-4","978-2-07-058021-7","978-2-07-079213-9","978-2-07-046969-7","978-2-07-046819-5","978-2-07-079347-1","978-2-07-046485-2","978-2-07-046824-9","978-2-07-079399-0","978-2-07-079395-2","978-2-07-079266-5","978-2-07-046956-7","978-2-07-046897-3","978-2-07-046795-2","978-2-07-046972-7","978-2-07-046872-0","978-2-07-046991-8","978-2-07-079270-2","978-2-07-046859-1","978-2-07-046970-3","978-2-07-077000-7","978-2-07-079345-7","978-2-07-046816-4","978-2-07-046870-6","978-2-07-046883-6","978-2-07-046921-5","978-2-07-046510-1","978-2-07-046889-8","978-2-07-046626-9","978-2-07-046827-0","978-2-07-046420-3","978-2-07-079388-4","978-2-07-079354-9","978-2-07-045873-8","978-2-07-046828-7","978-2-07-046801-0","978-2-07-046814-0","978-2-07-046809-6","978-2-07-046572-9","978-2-07-046810-2","978-2-07-046813-3","978-2-07-268826-3","978-2-07-058292-1","978-2-07-056014-1","978-2-07-079383-9","978-2-07-066882-3","978-2-07-059123-7","978-2-07-059968-4","978-2-07-059124-4","978-2-07-058293-8","978-2-07-058262-4","978-2-07-269323-6","978-2-07-046171-4","978-2-07-058253-2","978-2-07-055997-8","978-2-07-056000-4","978-2-07-078494-3","978-2-07-079277-1","978-2-07-046591-0","978-2-07-046935-2","978-2-07-065774-2","2-07-036905-6","978-2-07-046754-9","978-2-07-058867-1","978-2-07-046708-2","978-2-07-079362-4","978-2-07-077020-5","978-2-07-046871-3","978-2-07-046797-6","978-2-07-079406-5","978-2-07-019763-7","978-2-07-270410-9","978-2-07-046831-7","978-2-07-046159-2","978-2-07-079373-0","978-2-07-046230-8","978-2-07-270807-7","978-2-07-079368-6","978-2-07-079398-3","978-2-07-046770-9","978-2-07-046365-7","978-2-07-046711-2","978-2-07-046904-8","978-2-07-046901-7","978-2-07-079314-3","978-2-07-046987-1","978-2-07-046903-1","978-2-07-046538-5","978-2-07-046477-7","978-2-07-079228-3","978-2-07-079227-6","978-2-07-270808-4","978-2-07-270811-4","978-2-07-046932-1","978-2-07-046868-3","978-2-07078264-2","978-2-07-046905-5","978-2-07-046758-7","978-2-07-079403-4","978-2-07-270812-1","978-2-07-046753-2","978-2-07-046214-8","978-2-07-045916-2","978-2-07-046782-2","978-2-07-045912-4","978-2-07-270813-8","978-2-07-079382-2","978-2-07-046906-2","978-2-07-079402-7","978-2-07-046272-8","978-2-07-046930-7","978-2-07-270816-9","978-2-07-270809-1","978-2-07-270815-2","978-2-07-046222-3","978-2-07-077567-5","978-2-07-270810-7","978-2-07-045591-1","978-2-07-046936-9","978-2-07-079365-5","978-2-07-079360-0","978-2-07-079331-0","978-2-07-270814-5","978-2-07-079401-0","978-2-07-046899-7","2-07-037780-6","2-07-039379-8","978-2-07-045814-1","2-07-041753-0","2-07-040636-9","978-2-07-270539-7","978-2-07-063043-1","978-2-07-055585-7","978-2-07-507450-6","978-2-07-046741-9","978-2-07-046213-1","978-2-07-046712-9","978-2-07-046928-4","978-2-07-046351-0","978-2-07-034676-9","2-07-030654-2","978-2-07-046387-9","2-07-042527-4","2-07-030652-6","978-2-07-035921-9","2-07-030653-4","2-07-038104-8","978-2-07046612-2","978-2-07-046800-3","978-2-07-057884-9","978-2-07-066919-6","978-2-07-046403-6","978-2-07046818-8","978-2-07-046357-2","978-2-07-058852-7","978-2-07-079216-0","978-2-07-058320-1","978-2-07-060352-7","978-2-07-045410-5","2-07-037792-X","978-2-07-046436-4","978-2-07-046924-6","2-07-037625-7","978-2-07-046395-4","978-2-07-046829-4","978-2-07-046860-7","978-2-07-046887-4","978-2-07-046880-5","978-2-07-046511-8","978-2-07-046725-9","978-2-07-079319-8","978-2-07-079265-8","978-2-07-079263-4","978-2-07-046794-5","978-2-07-046882-9","978-2-07-079386-0","978-2-07-046273-5","978-2-07-017845-2","978-2-07-046622-1","2-07-033123-7","978-2-07-079279-5","978-2-07-079356-3","978-2-07-079390-7","978-2-07-046893-5","978-2-07-046881-2","978-2-07-046892-8","978-2-07-079392-1","978-2-07-077219-3","978-2-07-079311-2","978-2-07-045452-5","978-2-07-046888-1","978-2-07-046445-6","978-2-07-079348-8","978-2-07-046890-4","978-2-07-046922-2","978-2-07-058752-0","978-2-07-046933-8","978-2-07-041828-2","978-2-07-058296-9","2-07-042114-7","978-2-07-059024-7","978-2-07-059027-8","978-2-07-058829-9","978-2-07-059117-6","2-07-040111-1","2-07-040105-7","2-07-036158-6","2-07-030202-4","2-07-040884-1","2-07-038126-9","2-07-040468-4","2-07-040523-0","978-2-07-045105-0","2-07-038510-8","2-07-037471-8","2-07-037720-2","2-07-038228-1","2-07-033291-9","2-07-038063-7","2-07-041897-9","2-07-038406-3","2-07-033290-X","2-07-040505-2","2-07-057951-4","2-07-037908-6","2-07-040504-4","2-07-037886-1","2-07-040077-8","2-07-038886-7","2-07-036279-5","2-07-038735-6","2-07-037350-9","2-07-037613-3","2-07-040684-9","2-07-030978-9","2-07-030042-0","2-07-033290-X","978-2-07-044055-9","2-07-039271-6","2-07-041251-2","2-07-041950-9","2-07-037016-X","2-07-037244-8","2-07-033280-2","2-07-037055-0","2-07-038247-8","2-07-034264-0","2-07-036999-4","978-2-07-046138-7","978-2-07-034100-9","978-2-07-046858-4","978-2-07-271584-6","978-2-07-046421-0","978-2-07-046509-5","978-2-07-046740-2","978-2-07-046781-5","978-2-07-046409-8","978-2-07-066707-9","978-2-07-269314-4","978-2-07-046793-8","978-2-07-079332-7","978-2-07-079385-3","978-2-07-046238-4","978-2-07-269972-6","978-2-07-270534-2","978-2-07-046834-8","978-2-07-507463-6","978-2-07-059979-0","978-2-07-058856-5","978-2-07-065648-6","978-2-07-060159-2","978-2-07-058827-5","978-2-07-060163-9","2-07-036905-6","978-2-07-046841-6","978-2-07-058422-2","978-2-07-060154-7","978-2-07-507473-5","978-2-07-060000-7","978-2-07-060155-4","978-2-07-058377-5","978-2-07-058418-5","978-2-07-060348-0","978-2-07-060156-1","978-2-07-058421-5","978-2-07-046206-3","2-07-033440-6","978-2-07-046215-5","978-2-07-046211-7","978-2070467839","978-2-07-058857-2","978-2-07-078268-0","978-2-07-059977-6","2-07-040775-6","2-07-036188-8","2-07-037137-9","2-07-036633-2","2-07-031706-4","2-07-041087-0","978-2-07-058928-9","978-2-07-058930-2","978-2-07-058929-6","978-2-07-059077-3","978-2-07-059115-2","978-2-07-058933-3","978-2-07-061841-5","978-2-07-058267-9","978-2-07-058706-3","978-2-07-046912-3","978-2-07-058851-0","978-2-07-060140-0","978-2-07-059116-9","978-2-07-046919-2","978-2-07-078574-2","978-2-07-079312-9","978-2-07-079313-6","978-2-07-079400-3","978-2-07-044717-6","978-2-07-079211-5","978-2-07-046191-2","978-2-07-046224-7","978-2-07-079317-4","978-2-07-079375-4","978-2-07-079397-6","978-2-07-078208-6","978-2-07-046759-4","978-2-07-046918-5","978-2-07-046857-7","978-2-07-044363-5","978-2-07-046739-6","978-2-07-079219-1","978-2-07-045370-2","978-2-07-046737-2","978-2-07-078398-4","978-2-07-046791-4","978-2-07-079262-7","978-2-07-079226-9","978-2-07-046934-5","978-2-07-079374-7","978-2-07-079377-8","978-2-07-079316-7","978-2-07-078266-6","978-2-07-046837-9","978-2-07-079367-9","978-2-07-079282-5","978-2-07-041532-8","978-2-07-079315-0","978-2-07-079371-6","978-2-07-046917-8","978-2-07-046915-4","978-2-07-046973-4","978-2-07-046984-0","978-2-07-058363-8","978-2-07-035640-9","978-2-07-046315-2","2-07-031205-4","978-2-07-046840-9","2-07-050679-7","2-07-050678-9","978-2-07-062230-6","2-07-050673-8","978-2-07-079379-2","978-2-07-046788-4","978-2-07-079378-5","978-2-07-045917-9","978-2-07-045607-9","978-2-07-046780-8","978-2-07-039604-7","978-2-07-045982-7","978-2-07-045212-5","978-2-07-066704-8","978-2-07-066881-6","978-2-07-061713-5","978-2-07-270119-1","978-2-07-270549-6","978-2-07-057707-1","978-2-07-270554-0","978-2-07-269996-2","978-2-07-269991-7","978-2-07-270001-9","978-2-07-046736-5","978-2-07-270006-4","978-2-07-269651-0","2-07-033440-6","2-07-033451-1","978-2-07-269942-9","2-07-053586-X","978-2-07-044418-2","2-07-036170-5","2-07-042937-7","978-2-07-046838-6","2-07-032858-9","2-07-037524-2","978-2-07-046820-1","2-07-030799-9","978-2-07-060139-4","978-2-07-034274-7","2-07-051330-0","978-2-07-045451-8","978-2-07-043713-9","2-07-036911-0","2-07-038773-9","978-2-07-035666-9","2-07-032494-X","2-07-036191-8","978-2-07-044516-5","978-2-07-046898-0","2-07-051343-2","2-07-033440-6","2-07-051330-0","978-2-07-060161-5","978-2-07-272866-2","978-2-07-060160-8","2-07-033445-7","978-2-07-079372-3","978-2-07-066954-7","978-2-07-066659-1","2-07-040074-3","2-07-040038-7","2-07-039388-7","978-2-07-276148-5","978-2-07-046160-8","2-07-055263-2","2-07-039396-8","2-07-038419-5","2-07-037407-6","2-07-036688-X","2-07-055596-8","2-07-033384-1","2-07-039427-1","2-07-031202-X","2-07-058328-7","2-07-036969-2","2-07-034043-0","2-07-033403-1","978-2-07-044054-2","2-07-033445-7","2-07-040422-6","2-07-038747-X","2-07-036705-3","2-07-033296-9","978-2-07-036173-1","2-07-033405-8","2-07-037301-0","2-07-033291-8","2-07-033472-4","2-07-033538-0","2-07-038004-1","2-07-031122-8","2-07-036959-5","2-07-053886-9","2-07-033497-X","2-07-033330-2","2-07-037415-7","2-07-037229-4","2-07-036656-1","2-07-041031-5","978-2-07-270142-9","2-07-030941-X","2-07-031172-4","2-07-033420-1","2-07-031074-4","2-07-032479-6","2-07-033297-7","2-07-052826-X","2-07-037138-7","2-07-054352-8","978-2-07-034295-2","2-07-053676-9","2-07-033539-9","2-07-037912-4","978-2-07-034453-6","978-2-07-079394-5","978-2-07-079337-2","978-2-07-046873-7","978-2-07-046724-2","978-2-07-046822-5","978-2-07-269700-5","2-07-032913-5","978-2-07-079267-2","2-07-032374-9","978-2-07-079229-0","978-2-07-079217-7","978-2-07-079230-6","978-2-07-046925-3","978-2-07-046601-6","978-2-07-077259-9","978-2-07-046920-8","978-2-07-046907-9","978-2-07-06688-30","978-2-07-066953-0","978--2-07-066658-4","978-2-07-079235-1","978-2-07-269705-0","978-2-07-269072-3","978-2-07-046849-2","978-2-07-270395-9","978-2-07-270400-0","978-2-07-046848-5","978-2-07-046850-8","978-2-07-065036-1","2-07-037695-8","2-07-034015-5","2-07-038475-6","2-07-034032-5","2-07-037768-7","2-07-036797-5","2-07-033553-4","2-07-033451-1","2-07-051330-0","9782070793761","2-07-042822-2","978-2-07-045535-5","2-07-033497-X","978-2-07-056017-2","2-07-040443-9","978-2-07-058371-3","978-2-07-270011-8","978-2-07-270016-3","978-2-07-061255-0","978-2-07-061712-8","978-2-07-079396-9","978-2-07-046718-1","978-2-07-046856-0","2-07-033013-3","978-2-07-044206-5","978-2-07-046489-0","978-2-07-061277-2","978-2-07-065887-9","978-2-07-077697-9","978-2-07-060090-8","2-07032382-X","2-07-033433-3","978-2-07-039605-4","978-2-07-045791-5","978-2-07-044674-2","978-2-07-046559-0","978-2-07-045592-8","978-2-07-063204-6","978-2-07-064045-4","978-2-07-060426-5","2-07-037137-9","2-07-042161-9","2-07-037877-2","2-07-037877-2","2-07-039191-4","2-07-038524-8","2-07-051430-7","2-07-051329-7","978-2-07-046854-6","978-2-07-046852-2","978-2-07-046975-8","978-2-07- 046983-3","978-2-07-046916-1","978-2-07-055902-2","978-2-07-055903-9","2-07-041360-8","978-2-07-046962-8","978-2-07-066967-7","2-07-051587-7","2-07-031625-4","978-2-07-043900-3","978-2-07-057706-4","2-07-039412-3","978-2-07-034081-1","2-07-033894-0","978-2-07-061263-5","978-2-07035655-3","978-2-07-036317-9","978-2-07-507400-1","2-07-051339-4","2-07-033434-1","2-07-051337-8","2-07-042258-5","2-07-042260-7","978-2-07-079387-7","978-2-07-046776-1","978-2-07-079275-7","978-2-07-077133-2","978-2-07-079391-4","978-2-07-056017-2","978-2-07-046853-9","978-2-07-046909-3","978-2-07-058828-2","978-2-07-046851-5","978-2-07-046229-2","2-07-032374-9","2-07-033013-3","978-2-07-046913-0","978-2-07-046744-0","978-2-07-046728-0","2-07-042384-0","978-2-07-058998-2","978-2-07-059434-4","978-2-07-058997-5","978-2-07-044895-1","978-2-07-034441-3","2-07-051883-3","9782070469550","978-2-07-065064-4","2-07-031205-4","978-2-07-039649-8","978-2-07-035788-8","2-07-031807-9","2-07-030760-3","2-07-034264-0","978-2-07-270247-1","978-2-07-046245-2","978-2-07-079364-8","2-07-040020-4","978-2-07-046616-0","978-2-07-063200-8","978-2-07-062907-7","978-2-07-269812-5","978-2-07-044720-6","978-2-07-270529-8","978-2-07-035794-9","2-07-042232-1","2-07-041655-0","978-2-07-046260-5","2-07-037137-9","978-2-07-056016-5","2-07-058516-6","2-07-059545-5","2-07-052709-3","2-07-056964-0","2-07-033608-5","2-07-056711-7","2-07-051903-1","2-07-058767-3","2-07-059465-3","2-07-058441-0","2-07-056880-6","2-07-059337-1","2-07-036603-0","2-07-040879-5","2-07-033570-4","2-07-056787-7","2-07-051904-X","2-07-037707-5","2-07-033371-X","2-07-036539-5","2-07-033369-8","2-07-036424-0","2-07-033370-1","2-07-058765-7","2-07-032636-5","2-07-033159-8","2-07-052708-5","978-2-07-062725-7","2-07-036773-8","2-07-033611-5","2-07-056783-4","2-07-032934-8","2-07-040929-5","2-07-041824-3","2-07-052808-1","2-07-032575-X","2-07-051019-0","978-2-07-046855-3","978-2-07-046914-7","2-07-050680-0","2-07-034025-2","2-07-034027-9","2-07-033240-3","2-07-039475-1","2-07-038761-5","2-07-032901-1","2-07-036976-5","2-07-033281-0","2-07-040315-7","2-07-039320-8","2-07-037225-1 Le Vol.2 br.","2-07-037714-8","2-07-032646-2","2-07-037492-0","2-07-032726-4","2-07-054837-6","978-2-07-039904-8","978-2-07-043588-3","2-07-041297-0","978-2-07046596-5","978-2-07-077224-7","979-10-93457-04-8","978-2-07-078271-0","2-07-040743-8","978-2-07-039995-6","978-2-07-036430-5","978-2-07-046937-6","978-2-07-078326-7","978-2-07-046558-3","2-07-039388-7","2-07-050686-X","2-07-037860-8","2-07-036424-0","2-07-042223-2","2-07-050670-3","978-2-07-046768-6","978-2-07-036300-1","978-2-07-045397-9","2-07-036762-2","2-07-051329-7","2-07-036936-6","2-07-041368-3","2-07-037676-1","2-07-040945-7","2-07-040019-0","978-2-07-064739-2","2-07-036425-9","2-07-038962-6","2-07-038191-9","2-07-037069-0","978-2-07-046139-4","2-07-037237-5","978-2-07-064736-1","978-2-07-064737-8","978-2-07-064738-5","978-2-07-046908-6","2-07-032804-X","2-07-032471-0","978-2-07-077662-7","978-2-07-078581-0","978-2-07-078285-7","978-2-07-046911-6","978-2-07-079370-9","978-2-07-035690-4","978-2-07-046842-3","978-2-07-046910-9","2-07-031965-2","978-2-07-046833-1","2-07-036597-2","978-2-07-046846-1","978-2-07-036008-6","978-2-36279-249-6"]
#listeISBN = ["2-7441-7863-2"]

def isbn2genre(isbn):
    url_classify = "http://classify.oclc.org/classify2/Classify?isbn=" + isbn
    (test,result) = testURLetreeParse(url_classify)
    listeLCSH = []
    if (test):
        listeLCSH = isbn2lcsh(result)
    liste_rameau = [lcsh2rameau(el) for el in listeLCSH]
    liste_rameau = [el for el in liste_rameau if len(el) > 0]
    
    return liste_rameau

def isbn2lcsh(result):
    listeLCSH = []
    for lcsh in result.xpath("//classify:headings/classify:heading",namespaces=nsClassify):
            listeLCSH.append(lcsh.text.replace("--"," -- "))
    return listeLCSH

def lcsh2rameau(conceptLCSH):
    liste_uri = lcsh2rameau_from_data(conceptLCSH)
    if (liste_uri == []):
        liste_uri = lcsh2rameau_from_sru(conceptLCSH)
    return liste_uri

def lcsh2rameau_from_data(conceptLCSH):
    liste_uri = []
    conceptLCSH = conceptLCSH.replace('"','\"')
    query = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    select distinct ?libelleRameau ?concept where {
      {
      ?concept skos:altLabel \"""" +  conceptLCSH  + """\".
      } 
      UNION {
      ?concept skos:altLabel \"""" +  conceptLCSH + """\"@en.
      }
      ?concept skos:prelLabel ?libelleRameau.
    }
    """
    sparql.setQuery(query)
    try:
        sparql.setReturnFormat(JSON)
    except SPARQLExceptions.EndPointNotFound as err:
        print(err)
        print(query)
    try:
        results = sparql.query().convert()
        dataset = results["results"]["bindings"]

        for el in dataset:
            liste_uri.append(
                    [el.get("libelleRameau").get("value"),
                     el.get("concept").get("value").replace("#about","")
                     ]
                    )
        liste_uri = list(set(liste_uri))
    except error.HTTPError as err:
        print(err)
        print(query)
    except SPARQLExceptions.EndPointNotFound as err:
        print(err)
        print(query)
    return liste_uri

def lcsh2rameau_from_sru(conceptLCSH):
    liste_rameau = defaultdict(str)
    query = 'aut.equivalence adj "' + conceptLCSH + '"'
    url_sru = url_requete_sru(query,"intermarcxchange")
    (test,records) = testURLetreeParse(url_sru)
    if (test):
        for record in records.xpath("//mxc:record",namespaces=ns):
            ark = record.get("id")
            libelleRameau = []
            for f16X in record.xpath("mxc:datafield",namespaces=ns):
                tag = f16X.get("tag")
                if (tag[0:2]=="16"):
                    for subfield in f16X.xpath("mxc:subfield",namespaces=ns):
                        code = subfield.get("code")
                        val = subfield.text
                        libelleRameau.append("$"+code+" "+val)
            for f622 in record.xpath("mxc:datafield[@tag='622']", namespaces=ns):
                f622a = ""
                if (f622.find("mxc:subfield[@code='a']",namespaces=ns) is not None):
                    f622a = f622.find("mxc:subfield[@code='a']",namespaces=ns).text
                f622v = ""
                if (f622.find("mxc:subfield[@code='v']",namespaces=ns) is not None):
                    f622v = f622.find("mxc:subfield[@code='v']",namespaces=ns).text
                if (f622v == "LCSH"
                    and unidecode(f622a.lower()) == unidecode(conceptLCSH).lower()):
                    check_genre = check_genre_forme(record,ark)
                    if (check_genre):
                        liste_rameau[ark] = " ".join(libelleRameau)
    return liste_rameau

def check_genre_forme(record,ark):
    """Pour une notice Rameau en Intermarc, vérifie si la zone codée autorise 
    l'utilisation en genre/forme"""
    test = False
    value_genre_forme = record.find("mxc:controlfield[@tag='008']",namespaces=ns).text[62]
    if (value_genre_forme == "3"):
        test = True
    nna = ark[ark.find("ark:/12148/cb")+13:-1]
    if (nna in listeNNA_genres_formes):
        test = True
    return test
    


# =============================================================================
# Ensemble de fonctions utilitaires
# =============================================================================

def testURLetreeParse(url):
    test = True
    resultat = ""
    try:
        resultat = etree.parse(request.urlopen(url))
    except etree.XMLSyntaxError as err:
        print(url)
        print(err)
        test = False
    except etree.ParseError as err:
        print(url)
        print(err)
        test = False
    except error.URLError as err:
        print(url)
        print(err)
        test = False
    except ConnectionResetError as err:
        print(url)
        print(err)
        test = False
    except TimeoutError as err:
        print(url)
        print(err)
        test = False
    except http.client.RemoteDisconnected as err:
        print(url)
        print(err)
        test = False
    except http.client.BadStatusLine as err:
        print(url)
        print(err)
        test = False
    except ConnectionAbortedError as err:
        print(url)
        print(err)
        test = False
    return (test,resultat)

def url_requete_sru(query,recordSchema="unimarcxchange",maximumRecords="1000",startRecord="1"):
    url = urlSRUroot + urllib.parse.quote(query) +"&recordSchema=" + recordSchema + "&maximumRecords=" + maximumRecords + "&startRecord=" + startRecord
    return url

if __name__ == "__main__":
    outputfile = open("isbn2genre_resultats.txt","w",encoding="utf-8")
    for isbn in listeISBN:
        genre = isbn2genre(isbn)
        for el in genre:
            for key in el:
                outputfile.write("\t".join([isbn,key,el[key]]) + "\n")
                print(isbn,key,el[key])
        if (genre == []):
            outputfile.write(isbn + "\n")
            print(isbn)
            
