node('CAD') {
    try{
        veDir = "ve"
        withEnv([
                 "TEMP=${WORKSPACE}/tmp",
                 "TMP=${WORKSPACE}/tmp",
                 "JOB_NAME=BCDC_tests_build",
                 "VEDIR=${veDir}",
                 "PYLINTPATH=${WORKSPACE}/${veDir}/bin/pylint",
                 "MERGED_AND_CLOSED=''"
                 ]) {
           stage('checkout') {
               sh 'if [ ! -d "$TEMP" ]; then mkdir $TEMP; fi'
               checkout([$class: 'GitSCM', branches: [[name: '*/jf_dev']], doGenerateSubmoduleConfigurations: false, extensions: [], gitTool: 'Default', submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/bcgov/bcdc-test']]])                           
           }
           stage('parse webhook') {
               // get jq
               sh '''
               # Get JQ 
               if [ ! -f "./jq" ]; then
                   curl -o jq https://stedolan.github.io/jq/download/linux64/jq
                   chmod +x jq
               fi
               '''
               def merged_and_closed = sh returnStdout:true, script: '''
                    merged_and_close=false
                    jqeventref='.[28] | '
                    eventurl='https://api.github.com/repos/bcgov/bcdc-test/events?page=3'
                    eventjson=$(curl -sS $eventurl)
                    #echo curl -sS $eventurl 
                    #echo $jqeventref
                    #curl -sS $eventurl | ./jq "$jqeventref .type"
                    
                    # get the last event sent to github
                    eventtype=$(echo $eventjson | ./jq "$jqeventref .type" | tr -d '"')
                    #echo "eventtype is $eventtype"
                    
                    # if its a pr get the pr number
                    if [[ $eventtype = "PullRequestEvent" ]]; 
                    then
                       prnum=$(echo $eventjson | ./jq "$jqeventref .payload.number" | tr -d '"')
                       #echo prnum is $prnum
                       
                       # is the pr closed
                       action=$(echo $eventjson | ./jq "$jqeventref .payload.action" | tr -d '"')
                       #echo action is $action
                    
                       if [[ $action = "closed" ]];
                       then
                           # make sure its also merged
                           status_code=$(curl -s -o /dev/null -I -w "%{http_code}" https://api.github.com/repos/bcgov/bcdc-test/pulls/$prnum/merge)
                           #echo status_code is $status_code
                           if [ $status_code -eq  204 ];
                               then 
                                   merged_and_close=true
                           fi
                       fi
                    fi
               echo $merged_and_close
               '''
               echo "MERGED_AND_CLOSED=${merged_and_closed}"
               env.MERGED_AND_CLOSED = ${merged_and_closed}
               echo "done"                           
           }
           stage('test var') {
              echo "merge close value" + env.MERGED_AND_CLOSED
           }

           /*
           stage('prep Virtualenv') {
                sh 'if [ -d "ve_bcdc_test" ]; then rm -Rf ve_bcdc_test; fi'
                sh 'if [ -d "$VEDIR" ]; then rm -Rf $VEDIR; fi'
                sh  '''
                    [ -d data ] || mkdir data
                    export TMP=$WORKSPACE/data
                    export TEMP=$WORKSPACE/data
                    python -m virtualenv --clear $VEDIR
                    source $VEDIR/bin/activate
                    python --version
                
                    python -m pip install -U --force-reinstall pip || goto :error
                    python -m pip install --upgrade pip || goto :error
                    python -m pip install --no-cache-dir -r ./requirements.txt
                    python -m pip install --no-cache-dir -r ./requirements_build.txt
               '''
            }
           
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
                                curl $projectIdUrl --output projectId.json
                                pwd
                                ls -l
                            '''                            
                      
                            // Get the project id
                            pid = projectId()
                            echo "pid:" + pid
                            aid = analysisId(pid)
                            echo "aid:" + aid
                            env.qualityGateUrl = env.SONARURL + "/api/qualitygates/project_status?analysisId=" + aid
                      
                            sh 'curl  $qualityGateUrl -o qualityGate.json'
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
             */
        }
    } catch (e) {
        currentBuild.result = "FAILED"
        notifyFailed()
        throw e
    }
}
    
def projectId() {
        // curl on box doesn't seem to work with -u so doing this without creds 
        project = readJSON file: 'projectId.json'
        return project[ "current"][ "id" ]
       
}

def analysisId(id) {
    withCredentials([string(credentialsId: 'sonarToken', variable: 'sonarToken')]) {
        echo "input id:" + id
        env.taskIdUrl = env.SONARURL + "/api/ce/task?id=" + id
        sh 'curl $taskIdUrl -o taskId.json'
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