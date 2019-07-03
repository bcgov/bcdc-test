node('ETLdev') {
    try{
        winPaths=getWindowsPaths64()
        veDir = "ve"
        withEnv([
                 "TEMP=${WORKSPACE}/tmp",
                 "TMP=${WORKSPACE}/tmp",
                 "PATH+EXTRA=${winPaths}",
                 "JOB_NAME=BCDC_tests_build",
                 "VEDIR=${veDir}",
                 "PYLINTPATH=${WORKSPACE}\\${veDir}\\Scripts\\pylint.exe",
                 ]) {
            stage('checkout') {
                sh 'if [ ! -d "$TEMP" ]; then mkdir $TEMP; fi'
                checkout([$class: 'GitSCM', branches: [[name: "${env.TAGNAME}"]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: true, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], gitTool: 'Default', submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/bcgov/bcdc-test']]])                
            }
            stage('prep Virtualenv') {
                sh 'if [ -d "$VEDIR" ]; then rm -Rf $VEDIR; fi'
                bat '''
                    rmdir %VEDIR%
                    mkdir %WORKSPACE%\\data
                    set TMP=%WORKSPACE%\\data
                    set TEMP=%TMP%
                    
                    python -m virtualenv --clear %VEDIR% || goto :error
                    call %VEDIR%\\Scripts\\activate.bat || goto :error
                    
                    python --version
                    python -m pip install -U --force-reinstall pip || goto :error
                    python -m pip install --upgrade pip || goto :error
                    python -m pip install --no-cache-dir -r .\\requirements.txt || goto :error
                    python -m pip install --no-cache-dir -r .\\requirements_build.txt || goto :error
                    
                    :error
                    echo Failed with error #%errorlevel%.
                    exit /b %errorlevel%
                '''
            }
            stage ('Code Check'){
                tool name: 'appqa', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                withSonarQubeEnv('CODEQA'){
                  // Run the sonar scanner
                  bat 'sonar-scanner.bat -Dsonar.sources=. -Dsonar.projectKey=%JOB_NAME% -Dsonar.host.url=%SONARURL% -Dsonar.python.pylint=%PYLINTPATH% -Dsonar.login=%SONARTOKEN% -Dsonar.scm.exclusions.disabled=true'
                  // Get the project id
                  pid = projectId()
                  echo "pid:" + pid
                  aid = analysisId(pid)
                  echo "aid:" + aid
                  env.qualityGateUrl = env.SONARURL + "/api/qualitygates/project_status?analysisId=" + aid
                  
                  sh 'curl -u $SONARTOKEN: $qualityGateUrl -o qualityGate.json'
                  def qualitygate = readJSON file: 'qualityGate.json'
                  echo qualitygate.toString()
                  if ("ERROR".equals(qualitygate["projectStatus"]["status"])) {
                     error  "Quality Gate failure"
                  }
                      echo  "Quality Gate success"
                  } 
            }
            /*
            stage('Run') {
                bat '''
                    call %VEDIR%/Scripts/activate.bat || goto :error
                    python setup.py sdist bdist_wheel
                    python -m twine upload dist/*
                '''
            }*/ 
        }
    } catch (e) {
        currentBuild.result = "FAILED"
        notifyFailed()
        throw e
    }
}

def getWindowsPaths64() {
    myPath = ["E:\\sw_nt\\Git\\mingw64\\bin",
              "E:\\sw_nt\\oracle12c\\instantclient_12_2_32",
              "E:\\sw_nt\\Java\\jre1.8.0_161\\bin",
              "E:\\sw_nt\\Java\\jre1.8.0_161\\lib",
              "E:\\sw_nt\\python27\\ArcGIS10.5",
              "E:\\sw_nt\\python27\\ArcGIS10.5\\Scripts",
              "E:\\sw_nt\\arcgis\\Desktop10.5\\bin",
              "E:\\sw_nt\\arcgis\\Desktop10.5\\arcpy",
              "E:\\sw_nt\\arcgis\\Desktop10.5\\ArcToolbox\\Scripts",
              "E:\\sw_nt\\sonar-scanner\\bin", 
              "E:\\sw_nt\\sonar-scanner\\lib"
              ]
    myPathStr = myPath.join(';')
    return myPathStr }
    
def projectId() {
    env.projectIdUrl = env.SONARURL + "/api/ce/component?component=" + env.JOB_NAME
    sh 'curl -u $SONARTOKEN: $projectIdUrl -o projectId.json'
    project = readJSON file: 'projectId.json'
    return project[ "current"][ "id" ]
}

def analysisId(id) {
    echo "input id:" + id
    env.taskIdUrl = env.SONARURL + "/api/ce/task?id=" + id
    sh 'curl -u $SONARTOKEN: $taskIdUrl -o taskId.json'
    task = readJSON file: 'taskId.json'
    return task[ "task" ][ "analysisId" ]
}
    
def notifyFailed() {
    emailext (
        subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
        body: """FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' \n\n
              Check console output at ${env.BUILD_URL} ${env.JOB_NAME} [${env.BUILD_NUMBER}]  """,
        to: 'kevin.netherton@gov.bc.ca' 
    )
}