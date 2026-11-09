# Proof file: spot-check against the live site

Sample of 20 meetings and 33 documents from 2026-10, drawn with `random.seed(20261108)` (8 random meetings that have documents, 3 random meetings with none) plus deliberately chosen edge cases (the `why` column). This is a SAMPLE, not a full verification.
Method: each meeting page was fetched a second time and parsed with a separately written regex parser (the main scripts use BeautifulSoup); each document was downloaded a second time and its SHA-256 compared; page counts compared between poppler `pdfinfo` and `pypdf`.

## Meetings (our saved value vs. live page re-fetched)

| meeting | why sampled | date ours / live | requestor ours / live | docs ours / live | attendees ours / live | all match |
|---|---|---|---|---|---|---|
| [1533923](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=1557-AF41&meetingId=1533923) | random (with documents) | 10/14/2026 03:30 PM / 10/14/2026 03:30 PM | American Bankers Association / American Bankers Association | 1 / 1 | 10 / 10 | yes |
| [1551273](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0938-AV83&meetingId=1551273) | random (with documents) | 10/21/2026 10:00 AM / 10/21/2026 10:00 AM | Caly / Caly | 2 / 2 | 12 / 12 | yes |
| [1528274](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0910-ZD60&meetingId=1528274) | random (with documents) | 10/19/2026 10:30 AM / 10/19/2026 10:30 AM | FoodTrition Solutions LLC / FoodTrition Solutions LLC | 3 / 3 | 12 / 12 | yes |
| [1529623](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0584-AF17&meetingId=1529623) | random (with documents) | 10/16/2026 01:30 PM / 10/16/2026 01:30 PM | J.T.M. Provisions Co., Inc. dba J.T.M. Food Group / J.T.M. Provisions Co., Inc. dba J.T.M. Food Group | 1 / 1 | 4 / 4 | yes |
| [1545973](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0938-AV90&meetingId=1545973) | random (with documents) | 10/06/2026 11:30 AM / 10/06/2026 11:30 AM | PhRMA / PhRMA | 4 / 4 | 9 / 9 | yes |
| [1568673](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0938-AV83&meetingId=1568673) | random (with documents) | 10/20/2026 11:00 AM / 10/20/2026 11:00 AM | Liberty Partners Group / Liberty Partners Group | 3 / 3 | 15 / 15 | yes |
| [1515623](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=3010-AA10&meetingId=1515623) | random (with documents) | 10/13/2026 10:00 AM / 10/13/2026 10:00 AM | ASC Group, Inc. / ASC Group, Inc. | 1 / 1 | 6 / 6 | yes |
| [1581023](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=1670-AA04&meetingId=1581023) | random (with documents) | 10/21/2026 03:30 PM / 10/21/2026 03:30 PM | National Association of Manufacturers / National Association of Manufacturers | 1 / 1 | 9 / 9 | yes |
| [1588523](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0910-ZD94&meetingId=1588523) | random (no documents) | 10/27/2026 02:00 PM / 10/27/2026 02:00 PM | Alliance for Pharmacy Compounding / Alliance for Pharmacy Compounding | 0 / 0 | 10 / 10 | yes |
| [1535023](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0584-AF17&meetingId=1535023) | random (no documents) | 10/16/2026 01:00 PM / 10/16/2026 01:00 PM | National Pork Producers Council / National Pork Producers Council | 0 / 0 | 5 / 5 | yes |
| [1518523](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=3010-AA10&meetingId=1518523) | random (no documents) | 10/27/2026 10:30 AM / 10/27/2026 10:30 AM | Chronicle Heritage / Chronicle Heritage | 0 / 0 | 5 / 5 | yes |
| [1573623](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0938-AV82&meetingId=1573623) | edge: scanned/no-text PDF | 10/22/2026 11:00 AM / 10/22/2026 11:00 AM | Michael Best Strategies / Michael Best Strategies | 1 / 1 | 13 / 13 | yes |
| [1528824](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0910-ZD60&meetingId=1528824) | edge: PDF without filename header | 10/23/2026 01:00 PM / 10/23/2026 01:00 PM | Food is Medicine Institute at Tufts University / Food is Medicine Institute at Tufts University | 4 / 4 | 18 / 18 | yes |
| [1573774](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0910-AG30&meetingId=1573774) | edge: pptx | 10/15/2026 03:30 PM / 10/15/2026 03:30 PM | Covington & Burling LLP / Covington & Burling LLP | 1 / 1 | 16 / 16 | yes |
| [1515773](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=3010-AA10&meetingId=1515773) | edge: docx | 10/19/2026 02:00 PM / 10/19/2026 02:00 PM | National Alliance of Preservation Commissions / National Alliance of Preservation Commissions | 1 / 1 | 6 / 6 | yes |
| [1528723](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=1901-AB75&meetingId=1528723) | edge: xlsx | 10/13/2026 03:30 PM / 10/13/2026 03:30 PM | The Breakthrough Institute / The Breakthrough Institute | 5 / 5 | 7 / 7 | yes |
| [1526823](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0910-ZD60&meetingId=1526823) | edge: most documents | 10/15/2026 01:30 PM / 10/15/2026 01:30 PM | Nutrition scientists at University of California / Nutrition scientists at University of California | 5 / 5 | 15 / 15 | yes |
| [1524673](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2120-AL82&meetingId=1524673) | edge: status Scheduled | 10/08/2026 03:30 PM / 10/08/2026 03:30 PM | United Aerial Firefighters Association (UAFA) / United Aerial Firefighters Association (UAFA) | 0 / 0 | 0 / 0 | yes |
| [1515973](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=3010-AA10&meetingId=1515973) | edge: status No Show | 10/19/2026 02:30 PM / 10/19/2026 02:30 PM | Preservation Alliance of West Virginia / Preservation Alliance of West Virginia | 0 / 0 | 6 / 6 | yes |
| [1533723](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0910-ZD60&meetingId=1533723) | edge: last meeting of month by date | 10/30/2026 11:30 AM / 10/30/2026 11:30 AM | Betsy Booren / Betsy Booren | 0 / 0 | 0 / 0 | yes |

## Documents (first download vs. second download)

| document | meeting | file name | size | SHA-256 (first 12) | second-fetch SHA matches | pages pdfinfo / pypdf | text poppler / pypdf |
|---|---|---|---|---|---|---|---|
| [1428892](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1428892) | 1533923 | Deposit Flight and the MMF Parallel.docx | 19159 | d24d8e8dc11c | True |  /  | yes / n/a |
| [1431543](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1431543) | 1551273 | Calyxo_CMS_OPPS_ASC_CY27_PR_Cmt_ltr.pdf | 283568 | 017989ba469a | True | 7 / 7 | yes / yes |
| [1431542](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1431542) | 1551273 | Calyxo_OMB_issue_brief.pdf | 147501 | 2f7dd46aac27 | True | 1 / 1 | yes / yes |
| [1431346](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1431346) | 1528274 | That Post on Food Policy The Invisible Food Science Behind a Safe Nutritious Food Supply Dr. RC Post FoodTritionSolutions LLC September 18 2026.pdf | 253538 | ab0df5ea3a62 | True | 9 / 9 | yes / yes |
| [1431345](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1431345) | 1528274 | That Post on Food Policy- Food Policy Needs an Evidence Architecture Robert C. Post PhD FoodTrition Solutions LLC July 30 2026 Commentary.pdf | 2207159 | 5385e7ac3e48 | True | 8 / 8 | yes / yes |
| [1431342](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1431342) | 1528274 | OIRA_UPF_Submission on White Paper_Dr_Robert_Post_FoodTrition_Solutions_October 19 2026.pdf | 143960 | 9b9d25ff4f71 | True | 8 / 8 | yes / yes |
| [1429192](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1429192) | 1529623 | JTM_OMB_Testimony 10-16-26.pdf | 193397 | 572673277dbe | True | 6 / 6 | yes / yes |
| [1416442](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1416442) | 1545973 | CMS-2026-2080-0152_attachment_1.pdf | 940619 | d34a04480e93 | True | 78 / 78 | yes / yes |
| [1416443](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1416443) | 1545973 | 2026-10-6 EO 12866 Meeting on MDPNP Proposed Rule  - PhRMA .pdf | 335773 | 3efb0e1432de | True | 7 / 7 | yes / yes |
| [1416444](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1416444) | 1545973 | CMS-2026-2080-0151_attachment_1.pdf | 998837 | 74869d9c02c4 | True | 40 / 40 | yes / yes |
| [1416445](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1416445) | 1545973 | The Challenge of R&D Cost Reporting Under the IRA - Blue Matter Consulting copy.pdf | 5917195 | 5e6e56e82812 | True | 3 / 3 | yes / yes |
| [1431442](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1431442) | 1568673 | Fixing-the-Radiotherapy-Crosswalk-to-Protect-Patient-Access FINAL.pptx | 5292416 | 58177968a878 | True | 18 /  | yes / n/a |
| [1431443](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1431443) | 1568673 | American College of Radiation Oncology CY 2027 HOPPS Comment Letter FINAL (CMS-1850-P).pdf | 773506 | 12027bc39070 | True | 8 / 8 | yes / yes |
| [1431444](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1431444) | 1568673 | ACRO CY 2027 PFS Proposed Rule Comment Letter (CMS-1848-P).pdf | 508581 | 5dfc0189ac97 | True | 9 / 9 | yes / yes |
| [1423842](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1423842) | 1515623 | RIN 3010-AA10; E.O. 12866 - ASC Group Inc_.pdf | 591868 | 8f1c5e4ef2e5 | True | 4 / 4 | yes / yes |
| [1423992](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1423992) | 1581023 | 20240702 CIRCIA - NAM submission FINAL.pdf | 295990 | b4db780fa97a | True | 9 / 9 | yes / yes |
| [1436342](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1436342) | 1573623 | SWFP Comment Letter CMS.pdf | 5308319 | 44be9c9683e5 | True | 5 / 5 | no / no |
| [1436692](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1436692) | 1528824 | OMB-OIRA meeting_HHS-FDA proposed definition of UPF talking points_23 October 2026_for upload.pdf | 284722 | 441ff7ce64d7 | True | 6 / 6 | yes / yes |
| [1436693](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1436693) | 1528824 | (no filename header; title: AJPH.2026.UPF vs. Diet Quality in Relation to Cardiometabolic Health and All-Cause Mortality NHANES 1999–2018) | 879513 | 271b37871c38 | True | 10 / 10 | yes / yes |
| [1436694](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1436694) | 1528824 | Summary of Food is Medicine Institute response to FDA-USDA RFI on ultra-processed foods_Oct 2025.pdf | 221412 | 620fcd25f769 | True | 1 / 1 | yes / yes |
| [1436695](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1436695) | 1528824 | UPF science, medical, and nutrition experts sign-on letter to OMB_October 23, 2026_FINAL.pdf | 135234 | 8d9124ebb6c1 | True | 9 / 9 | yes / yes |
| [1426342](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1426342) | 1573774 | ASA OMB OIRA MEETING - FDA 1998-N-0880 - RIN 0910-AG30.pptx | 414120 | 46c0ef24a47a | True | 7 /  | yes / n/a |
| [1431492](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1431492) | 1515773 | NAPC OIRA Meeting Comments.docx | 3157318 | 4e22d040d519 | True |  /  | yes / n/a |
| [1423942](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1423942) | 1528723 | Sample-Size-Invariant Bias Wall.pdf | 430470 | b3879a1f265a | True | 23 / 23 | yes / yes |
| [1423943](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1423943) | 1528723 | Detectability Frontier of Low-Dose Radiation Epidemiology.pdf | 520577 | a802568affa1 | True | 14 / 14 | yes / yes |
| [1423944](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1423944) | 1528723 | BTI_Current State of Radiation Regulation.pdf | 177152 | ba48d6eb996e | True | 7 / 7 | yes / yes |
| [1423945](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1423945) | 1528723 | BTI-Radiation-Regulation-Spreadsheet.xlsx | 71613 | 0a6bee803691 | True |  /  | yes / n/a |
| [1423946](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1423946) | 1528723 | Breakthrough Institute Comment on Reforming and Modernizing the NRC Radiation Protection Framework.pdf | 427234 | af9cbdaed316 | True | 43 / 43 | yes / yes |
| [1429042](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1429042) | 1526823 | schmidt-2026-tobacco-industry-contributions.pdf | 1633807 | 2075a7b3529a | True | 10 / 10 | yes / yes |
| [1429043](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1429043) | 1526823 | niederdeppe-et-al-2026-public-awareness-and-support-for-governmental-intervention-to-address-harms-associated-with.pdf | 1358204 | 7a31420abc39 | True | 11 / 11 | yes / yes |
| [1429044](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1429044) | 1526823 | Ellison et al. - 2026 - The politics of processed foods Consumer perceptions of policies targeting ultra-processed foods.pdf | 627516 | c347a02be6a1 | True | 13 / 13 | yes / yes |
| [1429045](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1429045) | 1526823 | Paraje_e011312.full.pdf | 2837424 | f7a97f7cabfc | True | 11 / 11 | yes / yes |
| [1429046](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1429046) | 1526823 | USDA.UPF MTG_2026_Final.pdf | 199080 | fc4f02c8968c | True | 8 / 8 | yes / yes |

## Count reconciliation (full month, not a sample)

- Live banner 'Number Of Records Found' re-read at 2026-11-08 17:43:02 EST: 104.
- Our month list: 104 unique meeting ids (view-all pass and 10-per-page paginated pass returned identical id sets).
- Same search split into 5 date sub-ranges: banners sum to 104, union of ids = 104, identical to the month list: True. Day before (09/30) and day after (11/01) boundary checks returned 1 and 0 meetings (outside the month).
- Per-RIN cross-check (27 RINs, searched with no date filter, October rows counted): 104 meetings, id sets equal for every RIN: True. Limit: this can only find meetings on RINs already in the month list.
- EO review XML (rules under review + completed YTD, RUNDATE 2026-11-08): 27 of 27 month RINs appear. The XML has no meeting records, so this is plausibility only, not a count check.

# Full-range proof (2025-01-20 through 2026-11-08)

Sample of 60 meetings drawn with `random.seed(20261108)` from all 1380 stored meetings (50 random plus edge cases: no extracted text, no filename header, each file type present, most documents, Scheduled / No Show status, earliest and latest month), covering 17 months. Each was re-fetched live and compared field by field (date/time, requestor, requestor name, requestor client, title, document ids and titles, attendee count) with a separately written regex parser. This is a SAMPLE.
Result: 60 of 60 meetings match on every field. (A first run showed 12 requestor-name mismatches; the cause was my checker over-capturing the adjacent 'Requestor's Client' field, and it also exposed that the stored CSV lacked that field. I fixed the checker, added `requestor_client` to the CSVs by re-parsing saved HTML, and re-ran: 60 of 60.)
Documents: 36 of their documents were downloaded a second time; SHA-256 identical for 36 of 36; PDF page counts agree between pdfinfo and pypdf for 33 of 33 PDFs checked.

| meeting | month | why sampled | date | requestor | name | client | docs ours/live | attendees ours/live | all match |
|---|---|---|---|---|---|---|---|---|---|
| [1391823](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0938-AV98&meetingId=1391823) | 2026-05 | random | 05/15/2026 10:30 AM | Thorn Run Partners | Catherine Finley | Association for Behavioral Hea | 3/3 | 8/8 | yes |
| [1505873](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0584-AF17&meetingId=1505873) | 2026-08 | random | 08/11/2026 10:30 AM | American Bakers Association | Campbell Genn |  | 0/0 | 11/11 | yes |
| [1331773](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0584-AF12&meetingId=1331773) | 2026-03 | random | 03/12/2026 10:30 AM | National Association of Convenience Stor | Margaret Mannion |  | 2/2 | 11/11 | yes |
| [1376625](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=1018-BI76&meetingId=1376625) | 2026-05 | random | 05/08/2026 02:00 PM | Center for Biological Diversity | Stephanie Kurose |  | 0/0 | 5/5 | yes |
| [1457073](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=1840-AE06&meetingId=1457073) | 2026-06 | random | 06/26/2026 01:00 PM | American Association of Career Schools | John Russell |  | 1/1 | 5/5 | yes |
| [1540973](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0584-AF17&meetingId=1540973) | 2026-10 | random | 10/30/2026 10:00 AM | Plant Based Foods Association | Marjorie Mulhall |  | 0/0 | 12/12 | yes |
| [1024423](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0906-ZA14&meetingId=1024423) | 2025-07 | random | 07/10/2025 01:00 PM | RxParadigm Inc | Yogesh Arora |  | 1/1 | 13/13 | yes |
| [1533923](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=1557-AF41&meetingId=1533923) | 2026-10 | random | 10/14/2026 03:30 PM | American Bankers Association | Kaye Lynch-Sparks |  | 1/1 | 10/10 | yes |
| [993973](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0910-ZC21&meetingId=993973) | 2025-06 | random | 06/20/2025 01:30 PM | Trustwell | Katy Jones |  | 1/1 | 11/11 | yes |
| [1483423](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2127-AM76&meetingId=1483423) | 2026-07 | random | 07/21/2026 11:30 AM | Environmental Defense Fund | Andy Su |  | 0/0 | 8/8 | yes |
| [1096373](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2040-AG48&meetingId=1096373) | 2025-09 | random | 09/09/2025 02:30 PM | Talen Energy | Thomas Weissinger |  | 0/0 | 18/18 | yes |
| [1483373](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2040-AG44&meetingId=1483373) | 2026-08 | random | 08/03/2026 02:00 PM | American Petroleum Institute | Kelley Raymond |  | 0/0 | 22/22 | yes |
| [1113873](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0938-AV25&meetingId=1113873) | 2025-09 | random | 09/30/2025 11:30 AM | Senate Finance Committee | Kripa Sreepada |  | 0/0 | 11/11 | yes |
| [1001423](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2060-AW61&meetingId=1001423) | 2025-06 | random | 06/27/2025 10:30 AM | Sierra Club | Andres Restrepo |  | 0/0 | 6/6 | yes |
| [1434473](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2060-AW83&meetingId=1434473) | 2026-06 | random | 06/23/2026 01:30 PM | National Waste & Recycling Association | Kirk Sander |  | 0/0 | 6/6 | yes |
| [1376573](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0579-AE94&meetingId=1376573) | 2026-04 | random | 04/28/2026 03:30 PM | gabriella lara | gabriella lara |  | 0/0 | 0/0 | yes |
| [989323](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0694-AJ90&meetingId=989323) | 2025-06 | random | 06/12/2025 02:00 PM | lance raikoglo | lance raikoglo |  | 0/0 | 0/0 | yes |
| [1470023](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0938-AV74&meetingId=1470023) | 2026-07 | random | 07/23/2026 01:30 PM | Incyte Corporation | Stacie Abbott |  | 0/0 | 8/8 | yes |
| [1512423](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2120-AL82&meetingId=1512423) | 2026-08 | random | 08/27/2026 10:30 AM | Greenberg Traurig LLP | Joel Roberson | Sean Deverey at Honeywell Aero | 0/0 | 0/0 | yes |
| [1098874](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2040-AG48&meetingId=1098874) | 2025-09 | random | 09/05/2025 11:30 AM | DTE Energy | Matt Goddard |  | 0/0 | 12/12 | yes |
| [1350823](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=1004-AF33&meetingId=1350823) | 2026-04 | random | 04/13/2026 01:00 PM | Taxpayers for Common Sense | Tyler Work |  | 4/4 | 13/13 | yes |
| [1434623](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=3150-AL47&meetingId=1434623) | 2026-06 | random | 06/12/2026 01:00 PM | The Breakthrough Institute | Spencer Toohill |  | 5/5 | 12/12 | yes |
| [1001373](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0906-ZA14&meetingId=1001373) | 2025-07 | random | 07/02/2025 12:30 PM | 340B Health System Coalition | Devon Seibert-Bailey |  | 0/0 | 11/11 | yes |
| [1551123](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=1117-AB40&meetingId=1551123) | 2026-09 | random | 09/25/2026 01:30 PM | ATA Action | Joe Nye |  | 1/1 | 7/7 | yes |
| [1402023](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0970-AD34&meetingId=1402023) | 2026-05 | random | 05/27/2026 01:30 PM | Logan Braun | Logan Braun |  | 0/0 | 1/1 | yes |
| [1309123](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2050-AH39&meetingId=1309123) | 2026-03 | random | 03/06/2026 01:30 PM | John Ward Inc | John Ward | American Coal Ash Association | 2/2 | 9/9 | yes |
| [1488473](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0910-AI05&meetingId=1488473) | 2026-08 | random | 08/06/2026 11:00 AM | Campaign for Tobacco-Free Kids | Andrew Tardiff |  | 0/0 | 9/9 | yes |
| [1462773](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0596-AD66&meetingId=1462773) | 2026-07 | random | 07/13/2026 01:30 PM | Cascadia Wildlands | Grace Brahler |  | 0/0 | 4/4 | yes |
| [1515224](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0584-AF17&meetingId=1515224) | 2026-09 | random | 09/04/2026 02:30 PM | OFW Law | Roger Szemraj | Urban School Food Alliance | 0/0 | 7/7 | yes |
| [983923](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2120-AL33&meetingId=983923) | 2025-06 | random | 06/16/2025 01:30 PM | Hogan Lovells LLP | Hanson Causbie | Choctaw Nation | 0/0 | 21/21 | yes |
| [1284323](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=1235-AA46&meetingId=1284323) | 2026-02 | random | 02/05/2026 01:00 PM | National Demolition Association | Alex McIntyre |  | 0/0 | 12/12 | yes |
| [1024173](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2060-AW71&meetingId=1024173) | 2025-07 | random | 07/15/2025 02:00 PM | Natural Resources Defense Council (NRDC) | Atid Kimelman |  | 0/0 | 6/6 | yes |
| [1469423](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0906-ZA23&meetingId=1469423) | 2026-07 | random | 07/22/2026 02:30 PM | TDY@FGS | Jennifer Young | Christie Bloomquist at Boehrin | 0/0 | 10/10 | yes |
| [1518373](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=3010-AA10&meetingId=1518373) | 2026-10 | random | 10/27/2026 01:30 PM | History Colorado/Colorado State Historic | Annie Levinsky |  | 1/1 | 5/5 | yes |
| [1102723](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0938-AV73&meetingId=1102723) | 2025-12 | random | 12/12/2025 10:30 AM | The Legal Aid Society | Belkys Garcia |  | 1/1 | 6/6 | yes |
| [1505923](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0910-AJ27&meetingId=1505923) | 2026-08 | random | 08/13/2026 11:30 AM | Humane World Action Fund | Tracie Letterman |  | 1/1 | 6/6 | yes |
| [1511323](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0910-ZD60&meetingId=1511323) | 2026-08 | random | 08/19/2026 10:00 AM | American Bakers Association | Campbell Genn |  | 2/2 | 22/22 | yes |
| [1515773](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=3010-AA10&meetingId=1515773) | 2026-10 | random | 10/19/2026 02:00 PM | National Alliance of Preservation Commis | Stephanie Paul |  | 1/1 | 6/6 | yes |
| [1087224](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0938-AV73&meetingId=1087224) | 2025-08 | random | 08/28/2025 11:00 AM | Ethics and Public Policy Center | Rachel Morrison |  | 0/0 | 11/11 | yes |
| [1543325](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=1545-BS17&meetingId=1543325) | 2026-09 | random | 09/25/2026 03:00 PM | Christian Matozzo | Christian Matozzo |  | 0/0 | 4/4 | yes |
| [1457225](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0938-AV74&meetingId=1457225) | 2026-07 | random | 07/10/2026 02:00 PM | Stemline Therapeutics | Jay Greissing |  | 0/0 | 12/12 | yes |
| [968973](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2060-AW55&meetingId=968973) | 2025-06 | random | 06/06/2025 02:30 PM | Talley & Associates | Robert Talley | AFFORD Coalition | 0/0 | 11/11 | yes |
| [1521923](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0945-AA00&meetingId=1521923) | 2026-09 | random | 09/02/2026 03:30 PM | The Light Collective | Andrea Downing |  | 3/3 | 7/7 | yes |
| [1101523](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0938-AV25&meetingId=1101523) | 2025-09 | random | 09/15/2025 02:00 PM | American Health Care Association | Heather Posthumus |  | 0/0 | 10/10 | yes |
| [1101573](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2040-AG44&meetingId=1101573) | 2025-09 | random | 09/12/2025 11:30 AM | National Association of Home Builders | Evan Branosky |  | 0/0 | 13/13 | yes |
| [959224](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2060-AW23&meetingId=959224) | 2025-06 | random | 06/02/2025 11:00 AM | Renewable Fuels Association | Jared Mullendore |  | 0/0 | 8/8 | yes |
| [959323](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2060-AW23&meetingId=959323) | 2025-06 | random | 06/10/2025 11:00 AM | AJW, Inc. | Jordan Flanagan | Kinder Morgan | 0/0 | 8/8 | yes |
| [1421923](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=3150-AL47&meetingId=1421923) | 2026-06 | random | 06/16/2026 11:00 AM | Nuclear Innovation Alliance | Miranda McGuire |  | 1/1 | 11/11 | yes |
| [1067223](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2501-AE15&meetingId=1067223) | 2025-08 | random | 08/18/2025 01:30 PM | National Housing Law Project | Deborah Thrope |  | 0/0 | 9/9 | yes |
| [1361723](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=1685-AA38&meetingId=1361723) | 2026-04 | random | 04/28/2026 11:00 AM | International Mailers Advisory Group | Katherine Muth |  | 1/1 | 12/12 | yes |
| [1471923](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0579-AE93&meetingId=1471923) | 2026-07 | edge: no text extracted | 07/17/2026 02:00 PM | Humane World Action Fund; Humane World f | Drew Robertson |  | 2/2 | 11/11 | yes |
| [1274023](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=1235-AA46&meetingId=1274023) | 2026-01 | edge: no filename header | 01/29/2026 10:30 AM | U.S. Chamber of Commerce | Marc Freedman |  | 6/6 | 10/10 | yes |
| [916623](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0910-ZC19&meetingId=916623) | 2025-04 | edge: pptx | 04/29/2025 10:30 AM | King & Spalding | Jeffrey Shapiro | Artivion | 3/3 | 8/8 | yes |
| [1029273](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2060-AW71&meetingId=1029273) | 2025-07 | edge: docx | 07/24/2025 10:00 AM | Consumer Reports | Christopher Harto |  | 3/3 | 6/6 | yes |
| [1350223](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=1004-AF03&meetingId=1350223) | 2026-04 | edge: xlsx | 04/08/2026 01:30 PM | Defenders of Wildlife | Maddy Munson | Organizations that work and ha | 9/9 | 18/18 | yes |
| [961473](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2060-AW23&meetingId=961473) | 2025-06 | edge: doc | 06/11/2025 01:00 PM | Advanced Biofuel Association | Paul Argyropoulos | Michael McAdams | 2/2 | 7/7 | yes |
| [1419523](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=3060-AM01&meetingId=1419523) | 2026-06 | edge: most documents | 06/15/2026 01:30 PM | Landis+Gyr | Marguerite Behringer |  | 15/15 | 12/12 | yes |
| [1511874](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=2120-AL82&meetingId=1511874) | 2026-08 | edge: status Scheduled | 08/26/2026 01:00 PM | Wilkinson Barker Knauer | Kara Graves | CTIA | 0/0 | 0/0 | yes |
| [1294773](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0910-AJ02&meetingId=1294773) | 2026-02 | edge: status No Show | 02/20/2026 03:00 PM | Alaska Community Action on Toxins | Brittani Robbins |  | 0/0 | 2/2 | yes |
| [1591023](https://www.reginfo.gov/public/do/viewEO12866Meeting?viewRule=false&rin=0938-AV83&meetingId=1591023) | 2026-11 | edge: latest month | 11/04/2026 02:00 PM | LMH Strategic Solutions, LLC | Alanna Temme |  | 0/0 | 12/12 | yes |

## Documents re-downloaded

| document | meeting | file name | size | SHA-256 (12) | match | pages pdfinfo/pypdf |
|---|---|---|---|---|---|---|
| [1090792](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1090792) | 1274023 | (none) | 2051154 | 77c243307abb | True | 4/4 |
| [1090793](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1090793) | 1274023 | USCC comments on first Trump IC NPRM.pdf | 459490 | 41740b881c2e | True | 16/16 |
| [1090794](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1090794) | 1274023 | USCC Independent Contractor reg comments submitted.pdf | 420644 | 9bd1d424392d | True | 33/33 |
| [1090795](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1090795) | 1274023 | Ex. A - Ready_fire_aim_report_on_the_gig_economy.pdf | 366207 | 3b5fc0d0a901 | True | 52/52 |
| [1090796](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1090796) | 1274023 | U.S. Chamber Praises Pause on Enforcement of Biden-Era Independent Contractor Rule  _ U.S. Chamber of Commerce.pdf | 121953 | 411812babcba | True | 3/3 |
| [1090797](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1090797) | 1274023 | (none) | 1965608 | 6e23fefd3d08 | True | 6/6 |
| [1179142](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1179142) | 1350223 | (none) | 9362560 | 048bb1fd7505 | True | 292/292 |
| [1179143](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1179143) | 1350223 | (none) | 8127155 | 526867564841 | True | 129/129 |
| [1179144](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1179144) | 1350223 | (none) | 6343847 | 9cd92fdc8175 | True | 177/177 |
| [1179145](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1179145) | 1350223 | (none) | 9510162 | df422b49a5c1 | True | 184/184 |
| [1179146](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1179146) | 1350223 | (none) | 6093440 | 77cff328e3bd | True | 92/92 |
| [1179147](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1179147) | 1350223 | (none) | 9948572 | 8ba2416cdf09 | True | 653/653 |
| [1179148](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1179148) | 1350223 | (none) | 4965230 | 381d816115ee | True | 87/87 |
| [1179149](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1179149) | 1350223 | (none) | 6666462 | 0ebcda365eee | True | 157/157 |
| [1179150](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1179150) | 1350223 | 3-26-2026-AIM-Composite-Data-from-2022-2024-Locked.xlsx | 73582 | 506d8c339270 | True | / |
| [1288542](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288542) | 1419523 | 24-240.pdf | 118981 | 7c91a7970667 | True | 49/49 |
| [1288543](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288543) | 1419523 | 2024-9 -- Petition Opposition .pdf | 220873 | b4fd8d16f3cd | True | 7/7 |
| [1288544](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288544) | 1419523 | 2024-9 -- Petition Reply Comments.pdf | 322946 | 882f8db3574f | True | 14/14 |
| [1288545](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288545) | 1419523 | 2025-3 -- NOI Ex Parte pdf.pdf | 121221 | 945f7c43ee48 | True | 1/1 |
| [1288546](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288546) | 1419523 | 2025-4 -- HFR Economic Study.pdf | 666175 | 7124dec7de26 | True | 38/38 |
| [1288547](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288547) | 1419523 | 2025-4 -- NOI Comments.pdf | 259102 | 34c5518b5af2 | True | 9/9 |
| [1288548](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288548) | 1419523 | 2025-5 -- HFR Deck.pdf | 1709855 | 702bb5d377b2 | True | 11/11 |
| [1288549](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288549) | 1419523 | 2025-5 -- HFR Ex Parte.pdf | 541376 | 8e46772d1e6c | True | 2/2 |
| [1288550](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288550) | 1419523 | 2025-12 -- Neology Tech Study.pdf | 1897236 | 5860f97fc8f2 | True | 41/41 |
| [1288551](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288551) | 1419523 | 2025-12 -- Sturza Tech PPT.pdf | 139253 | 2ae084b7b7e4 | True | 7/7 |
| [1288552](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288552) | 1419523 | 2026-3 -- Cover Letter Tech Reply to NextNav.pdf | 92536 | 019f7e17d091 | True | 1/1 |
| [1288553](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288553) | 1419523 | 2026-3 -- Tech Reply to NextNav.pdf | 938567 | 52b91ca67838 | True | 35/35 |
| [1288554](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288554) | 1419523 | 2026-3 -- Tech Reply to NextNav.pdf | 938567 | 52b91ca67838 | True | 35/35 |
| [1288555](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288555) | 1419523 | Lower 900 MHz Band One Pager 2.10.26.docx | 21972 | c054bf18a1c1 | True | / |
| [1288556](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1288556) | 1419523 | Neology_Reponse_To_NextNav_Jan15_Filing_2600319[95] (1).pdf | 938567 | 52b91ca67838 | True | 35/35 |
| [1303642](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1303642) | 1471923 | investigation-report-tn-cruel-training-walking-horse.pdf | 349597 | 02296f586759 | True | 3/3 |
| [1303643](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=1303643) | 1471923 | investigation-documents-horse-abuse.pdf | 1509411 | dcd148584d60 | True | 7/7 |
| [828342](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=828342) | 916623 | Letter to FDA re Mtb and Sepsis Guidances STS AATS CHSS.pdf | 225833 | 111752d9dae3 | True | 2/2 |
| [828343](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=828343) | 916623 | Artivion OMB presentation 4.29.2025 v2.pdf | 404682 | efbc2b6434b4 | True | 14/14 |
| [828344](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=828344) | 916623 | Artivion OMB presentation 4.29.2025 v2.pptx | 2486054 | b1e52d783e2e | True | 14/ |
| [873242](https://www.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=873242) | 961473 | GD_Lipid Feedstocks Outlook to 2030_June 2025.pdf | 1388571 | a9c357e9faf8 | True | 14/14 |

## Per-month banner vs ours vs second count

Banner = site's 'Number Of Records Found' for that month's date range (2025-01 starts 01/20; 2026-11 ends 11/08). Second count = the same range searched as 7-day sub-ranges, banners summed and ids unioned. Also in `data/monthly_reconciliation.csv`.

| month | banner | ours (distinct ids) | sub-range sum | union equals ours | documents listed |
|---|---|---|---|---|---|
| 2025-01 | 0 | 0 | 0 | True | 0 |
| 2025-02 | 1 | 1 | 1 | True | 0 |
| 2025-03 | 25 | 25 | 25 | True | 47 |
| 2025-04 | 21 | 21 | 21 | True | 26 |
| 2025-05 | 42 | 42 | 42 | True | 34 |
| 2025-06 | 85 | 85 | 85 | True | 64 |
| 2025-07 | 75 | 75 | 75 | True | 66 |
| 2025-08 | 66 | 66 | 66 | True | 36 |
| 2025-09 | 93 | 93 | 93 | True | 56 |
| 2025-10 | 0 | 0 | 0 | True | 0 |
| 2025-11 | 0 | 0 | 0 | True | 0 |
| 2025-12 | 53 | 53 | 53 | True | 53 |
| 2026-01 | 68 | 68 | 68 | True | 91 |
| 2026-02 | 64 | 64 | 64 | True | 61 |
| 2026-03 | 88 | 88 | 88 | True | 67 |
| 2026-04 | 92 | 92 | 92 | True | 142 |
| 2026-05 | 98 | 98 | 98 | True | 84 |
| 2026-06 | 87 | 87 | 87 | True | 101 |
| 2026-07 | 81 | 81 | 81 | True | 83 |
| 2026-08 | 103 | 103 | 103 | True | 99 |
| 2026-09 | 122 | 122 | 122 | True | 143 |
| 2026-10 | 104 | 104 | 104 | True | 99 |
| 2026-11 | 12 | 12 | 12 | True | 19 |
