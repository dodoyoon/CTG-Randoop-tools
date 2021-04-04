# CTG-Randoop-tools
Tools used for CTG-Randoop(Continuous Unit Test Generation with Randoop)


![diagram](https://github.com/dodoyoon/CTG-Randoop-tools/blob/main/diagram.png)

## CTG-Randoop
CTG-Randoop, short for 'Continuous Unit Test Generation with Randoop', is a framework to allow automated continuous testing of a project, only notifying of newly-detected errors to the user. It integrates Github-Jenkins-Gerrit to automatically report newly-detected error on a new version to the team. This framework requires running Jenkins and Gerrit server. 

<br>


## Tools / Scripts Used
### extract_dictionary.py
Python module to extract keywords from the given source code to use as Randoop test's seeds. When given input of source code path, it produces text file named 'literalsfile.txt' which contains seed constants to be used for testing of each class. 
```
python3 extract_dictionary.py [source code path] [save file path]
```

### filter_result.py
Python module to compare two versions to randoop testing, which are given as JSON format, and provide result of only new errors in the most recent version, depending on the heuristic chosen (10 heuristics given). 
```
python3 filter_result.py [json of previous version] [json of current version] [heuristic number] [commit hash previous version] [commit has current version] [path to current directory] [gerrit server address] [number of results](optional)
```

### Jenkinsfile
Example of Jenkinsfile to be used for Jenkins Pipeline. Pipeline allows users to view real-time update of the CTG-Randoop process. This file can be used by Jenkins via GUI on Jenkins server. Alteration of information(e.g. paths) are needed before use. 

## Related
[UCC](https://youtu.be/Z-s_1L4BmTk) | [Demo Video](https://youtu.be/kZ2xz8AQ3Aw) | [Paper](http://ksc2020.kiise.or.kr/wp/popPDF.asp?p=jncAE2qcBEA1CDPjT0QTWer1CVL0x1HejxX0G06Lc4lvOqS0QmlOw1v5gXc2)



## Setup Guides
[Jenkins](https://www.jenkins.io/doc/book/installing/linux/) <br>
[Gerrit](https://gerrit-review.googlesource.com/Documentation/)
