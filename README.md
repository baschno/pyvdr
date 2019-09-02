# pyvdr
Python library for accessing a Linux VDR via SVDRP

[![CircleCI](https://circleci.com/gh/baschno/pyvdr/tree/master.svg?style=svg)](https://circleci.com/gh/baschno/pyvdr/tree/master)

```
220 easyVDR SVDRP VideoDiskRecorder 2.2.0; Sat Dec  8 19:21:38 2018; UTF-8
250 Message queued
221 easyVDR closing connection
```

## SVDRP
### Parsing of Responses
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

LSTE 2 now
```
215-C C-102-1079-11110 ZDF HD
215-E 45654 1544564700 4500 4E 4
215-T Markus Lanz
215-D Ole von Beust, Politiker - Hamburgs ehemaliger Erster Bürgermeister sagt: "Der Wahlkampf hat belebend gewirkt." Von Beust erklärt, warum er mit dem Ergebnis zufrieden ist und wie der Aufbruch in der CDU gelingen kann.|Kristina Dunz, Journalistin - Auch sie war beim CDU-Parteitag in Hamburg und sagt: "Es geht ein Riss durch die Christdemokraten." In der Sendung erzählt Dunz, wie sie die Stimmung in der Partei vor Ort erlebt hat.|Wolfgang Grupp, Unternehmer - Er sprach sich im Vorfeld offen für Friedrich Merz als Parteivorsitzenden aus. Grupp sagt: "Die Chance auf einen Kurswechsel der CDU wurde vertan." Der Unternehmer gibt seine Einschätzung.|Benedikt Böhm, Speedbergsteiger - Der Extrembergsteiger weiß: "Der Tod ist Teil des Sports." In der Sendung erklärt Böhm, warum der Tod immer eine Option ist, und erzählt von seiner Speedbesteigung des Mount Damavand. Moderation: Markus Lanz|HD-Produktion|Altersfreigabe: 6
215-G 80
215-X 2 03 deu Stereo
215-X 2 03 mul ohne Originalton
215-X 2 03 mis ohne Audiodeskription
215-X 2 03 deu Dolby Digital 2.0
215-X 5 0B deu HDTV
215-X 3 10 deu DVB-Untertitel
215-V 1544564700
215-e
215-c
215 End of EPG data
```
```
215-e
215-E 4603 1545174000 3600 51 6
215-T CNN Today (with World Sport)
215-D CNN's Michael Holmes and Amara Walker from Atlanta, set the agenda for the day's most important news, business and sport stories.
215-G 20
215-e
215-c
```

### Chan
```
250 2 ZDF HD
```


### Timers

Plain response
```
250-1 1:3:2018-12-12:2013:2330:50:99:The Taste~Es weihnachtet sehr! Acht ehemalige Schützlinge der Coaches Cornelia Poletto, Alexander Herrmann, Frank Rosin und Roland Trettl kochen bei der grossen Weihnachtsspezial-Challenge.:<epgsearch><channel>3 - SAT.1</channel><searchtimer>The taste</searchtimer><start>1544641980</start><stop>1544653800</stop><s-id>4</s-id><eventid>4353</eventid></epgsearch>
```

#### Status Flags
Flags in timer definition
```
1   the timer is active (and will record if it hits)
2   this is an instant recording timer
4   this timer uses VPS
8   this timer is currently recording (may only be up-to-date with SVDRP)
```
Those flags are bit-representations in the timers' status field.


## Module lifecycle
### Build module
```
python3 setup.py sdist bdist_wheel
```

### Install module
To manually install:
```
pip install pyvdr/dist/pyvdr-0.1.2-py3-none-any.whl --upgrade
```

### Upload
After setup of an configuration file `~/.pypirc`:
```
python -m twine upload dist/*
```

```
netcat -w 10 vdr.local 6419 <<EOF
chan
quit
EOF
220 easyVDR SVDRP VideoDiskRecorder 2.2.0; Sun Sep  1 15:27:23 2019; UTF-8
250 66 Disney SD
221 easyVDR closing connection
```

## Resources
Create a python module https://dzone.com/articles/executable-package-pip-install
