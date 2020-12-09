pipeline { 
    agent any  
    tools{
        maven 'Maven 3.6'
    }
    stages { 
        stage('Build') { 
            steps { 
               sh 'mvn package -Dmaven.test.skip=true' 
            }
        }

        stage('Test'){
            steps{
                sh script:'''
                export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
                export PATH=$PATH:$JAVA_HOME/bin
                export JUNIT_HOME=/usr/share/java
                export CLASSPATH=$CLASSPATH:$JUNIT_HOME/junit4.jar
                export JUNITPATH=$CLASSPATH:$JUNIT_HOME/junit4.jar:$CLASSPATH:$JUNIT_HOME/hamcrest-core-1.3.jar
                export RANDOOP_PATH=/home/kaydeee329/shift
                export RANDOOP_JAR=/home/kaydeee329/shift/randoop-all-4.2.3.jar

                cd randoop
                . ./randoop.sh || true

                javac -classpath .:$JUNITPATH ErrorTest*.java RegressionTest*.java || true
                java -classpath .:$JUNITPATH: org.junit.runner.JUnitCore ErrorTest > $(git rev-parse --show-toplevel)/randoop/err$BUILD_NUMBER.md || true
                java -classpath .:$JUNITPATH: org.junit.runner.JUnitCore RegressionTest > $(git rev-parse --show-toplevel)/randoop/reg$BUILD_NUMBER.md || true

                rm ErrorTest*
                rm RegressionTest* || true
                '''
            }
        }
        
        stage('Filter & Result'){
            steps{
                sh script:'''
                git push gerrit HEAD:refs/for/test
                cd $(git rev-parse --show-toplevel)/randoop

                python3 /home/kaydeee329/CTG-Randoop/randoop2json.py $(pwd)/err$BUILD_NUMBER.md
                python3 /home/kaydeee329/CTG-Randoop/filter_result.py $(pwd)/err$(( ${BUILD_NUMBER#0} -1 )).md.json $(pwd)/err$BUILD_NUMBER.md.json 4 $(git rev-parse HEAD^1) $(git rev-parse HEAD) $(git rev-parse --show-toplevel)/src/main/java/org kaydeee329@localhost 3 || true
                '''
            }
        }
    }
}

