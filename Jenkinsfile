node('master') {
    try{
        veDir = "ve"
        withEnv([
                 "TEMP=${WORKSPACE}/tmp",
                 "TMP=${WORKSPACE}/tmp",
                 "JOB_NAME=BCDC_tests_build",
                 "VEDIR=${veDir}",
                 "PYLINTPATH=${WORKSPACE}/${veDir}/Scripts/pylint.exe",
                 ]) {
            stage('checkout') {
                sh 'if [ ! -d "$TEMP" ]; then mkdir $TEMP; fi'
                checkout([$class: 'GitSCM', branches: [[name: "${env.TAGNAME}"]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: true, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], gitTool: 'Default', submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/bcgov/bcdc-test']]])                
            }
           // stage('prep Virtualenv') {
           //     sh 'if [ -d "ve_bcdc_test" ]; then rm -Rf ve_bcdc_test; fi'
           //     sh 'if [ -d "$VEDIR" ]; then rm -Rf $VEDIR; fi'
           //     sh  '''
           //         [ -d data ] || mkdir data
           //         export TMP=$WORKSPACE/data
           //         export TEMP=$WORKSPACE/data
           //         python -m virtualenv --clear $VEDIR
           //         source $VEDIR/bin/activate
           //         python --version
           //     '''
                // comment out while work on other stages...
                    //python -m pip install -U --force-reinstall pip || goto :error
                    //python -m pip install --upgrade pip || goto :error
                    //python -m pip install --no-cache-dir -r ./requirements.txt
                    //python -m pip install --no-cache-dir -r ./requirements_build.txt
            //}
            stage ('SonarScan'){
                withCredentials([string(credentialsId: 'sonarToken', variable: 'sonarToken')]) {
                    withEnv(['PATH=/apps/download/n/8/bin:/s00/bin:/apps/sonarscanner/bin:/bin:/usr/bin:/s00/libexec/git-core', 'LD_LIBRARY_PATH=/apps/download/n/8/lib:/s00/lib64:/apps/sonarscanner/lib:/lib64:/usr/lib64']) {
                        tool name: 'sonarscanner'
                        withSonarQubeEnv('CODEQA'){
                        //  Run the sonar scanner
                            env.projectIdUrl = env.SONARURL + "/api/ce/component?component=" + env.JOB_NAME
                            sh '''
                                [ -d $TMP ] || mkdir $TMP
                                sonar-scanner -Dsonar.sources=. -Dsonar.projectKey=$JOB_NAME -Dsonar.host.url=$SONARURL -Dsonar.python.pylint=$PYLINTPATH -Dsonar.login=${sonarToken}  -Dsonar.exclusions=ve/**,build/**
                                echo "tokenlength: ${#sonarToken}"
                                echo $projectIdUrl
                                curl --version
                                curl -o $TMP/junk.json -u ${sonarToken}: $projectIdUrl 
                                pwd
                                ls -l
                                ls -l $TMP
                            '''
                            sh 'curl -o junk.json -u ${sonarToken}: $projectIdUrl' 
                            
                      
                            // Get the project id
                            pid = projectId('projectId.json')
                            echo "pid:" + pid
                            aid = analysisId(pid)
                            echo "aid:" + aid
                            env.qualityGateUrl = env.SONARURL + "/api/qualitygates/project_status?analysisId=" + aid
                      
                            sh 'curl -u ${sonarToken}: $qualityGateUrl -o qualityGate.json'
                            def qualitygate = readJSON file: 'qualityGate.json'
                            echo qualitygate.toString()
                            if ("ERROR".equals(qualitygate["projectStatus"]["status"])) {
                                error  "Quality Gate failure"
                            }
                            echo  "Quality Gate success"
                        }
                    }
                }
            }
            stage('Build') {
                sh '''
                    source $VEDIR/bin/activate
                    python setup.py sdist bdist_wheel
                    python -m twine upload dist/*
                '''
            }
        }
    } catch (e) {
        currentBuild.result = "FAILED"
        notifyFailed()
        throw e
    }
}
    
def projectId(projectid) {
    //withCredentials([string(credentialsId: 'sonarToken', variable: 'sonarToken')]) {
        //sh 'echo "tokenlength: ${#apiToken}"'
        //env.projectIdUrl = env.SONARURL + "/api/ce/component?component=" + env.JOB_NAME
        //sh 'curl -u $apiToken: $projectIdUrl -o projectId.json'
        project = readJSON file: 'projectId.json'
        return project[ "current"][ "id" ]
    //}
       
}

def analysisId(id) {
    withCredentials([string(credentialsId: 'sonarToken', variable: 'sonarToken')]) {
        echo "input id:" + id
        env.taskIdUrl = env.SONARURL + "/api/ce/task?id=" + id
        sh 'curl -u ${sonarToken}: $taskIdUrl -o taskId.json'
        task = readJSON file: 'taskId.json'
        return task[ "task" ][ "analysisId" ]
    }
}
    
def notifyFailed() {
    emailext (
        subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
        body: """FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' \n\n
              Check console output at ${env.BUILD_URL} ${env.JOB_NAME} [${env.BUILD_NUMBER}]  """,
        to: 'kevin.netherton@gov.bc.ca' 
    )
}