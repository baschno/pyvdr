# pyvdr
Python library for accessing a Linux VDR via SVDRP

```
220 easyVDR SVDRP VideoDiskRecorder 2.2.0; Sat Dec  8 19:21:38 2018; UTF-8
250 Message queued
221 easyVDR closing connection
```


## Parsing of Responses
The first and the last row just contain a ' ' as separator while other have a '-'.

Example:
```
[
('220', ' ', 'easyVDR SVDRP VideoDiskRecorder 2.2.0; Sun Dec  9 21:17:06 2018; UTF-8\r'), 
('215', '-', 'C C-9999-161-12103 ProSieben'), 
('215', '-', 'E 4321 1544382900 7500 4E 16'), 
('215', '-', 'T The Jungle Book'), 
('215', '-', 'S Abenteuer-Realfilm. Der kleine Mogli wird im Dschungel von W\xc3\xb6lfen aufgezogen. Als sein Leben durch den Tiger Shir Khan bedroht wird, muss er zu den Menschen zur\xc3\xbcckkehren.'), ('215', '-', 'D Abenteuer-Realfilm. Der Junge Mogli ist im Indischen Dschungel von W\xc3\xb6lfen gro\xc3\x9fgezogen worden. Doch dann bedroht der Tiger Shir Khan sein Leben und er muss seine Familie verlassen. Gemeinsam mit seinen Begleitern, dem strengen Panther Baghira und dem lebenslustigen B\xc3\xa4ren Balu, macht er sich auf den Weg zu den Menschen. Zusammen m\xc3\xbcssen sie ein Abenteuer voller Gefahren bestehen. So hat es unter anderem die Schlange Kaa auf Mogli abgesehen und auch der Affenk\xc3\xb6nig Louie ist hinter ihm her. Louie will ihm entlocken, wie man Feuer macht, um den Menschen so \xc3\xa4hnlich wie m\xc3\xb6glich zu werden. Doch auch Shir Khan ist den drei Freunden immer dicht auf den Fersen. Er will Mogli daran hindern, das Menschendorf zu erreichen. IMDb rating: 7.4/10.|Role Player: Neel Sethi|Director: Jon Favreau|Scriptwriter: Justin Marks|Producer: Brigham Taylor'), 
('215', '-', 'G 12'), 
('215', '-', 'e'), 
('215', '-', 'c'), 
('215', ' ', 'End of EPG data\r')]
```