def fullBranchUrl(branchName) { return "${scm.getUserRemoteConfigs()[0].getUrl()}/tree/$branchName" }

def getBranchName() { 
    if(env.CHANGE_ID != null) {
        return 'remote-trigger'
    } else {
        return 'master'
    }

}

def getGitUrl() {
    if(env.CHANGE_ID != null) {
        return 'https://github.com/tilsharm-testorg/gh-pr-test.git'
    } else {
        return 'https://github.com/TilakShrma/gh-pr-test.git'
    }
}

def trigger_external_job(param) {
    build job: '/tests/e2e_suit/e2e_scan_test/', parameters: [string(name: 'env', value: param)], propagate: false, wait: false
}

timestamps {
    node(label: 'master') {
        stage('Checkout Git Repo') {
            git credentialsId: 'fe4effdc-f62d-4624-bcc7-d4749675f873',
            branch: getBranchName(),
            url: getGitUrl()
        }
        // stage('Archive and Record Tests') {
        //     if (fileExists('output/coverage/jest/cobertura-coverage.xml') && fileExists('output/coverage/jest/jest-junit.xml')) {
        //         archiveArtifacts 'output/coverage/jest/cobertura-coverage.xml'
        //         archiveArtifacts 'output/coverage/jest/jest-junit.xml'
        //         cobertura coberturaReportFile: 'output/coverage/jest/cobertura-coverage.xml'
        //     }
        //     else {
        //         echo 'XML report were not created'
        //     }
        // }
        // stage('Parse Xml'){
        //     if(env.CHANGE_ID != null){
        //         copyArtifacts filter: 'output/', projectName: 'master', selector: lastCompleted(), target: 'master/'
        //         try{
        //             powershell "C:/Python27/python.exe ./bin/xmlToJson.py master/output/coverage/jest/cobertura-coverage.xml --type=cobertura"
        //             powershell "C:/Python27/python.exe ./bin/xmlToJson.py master/output/coverage/jest/jest-junit.xml --type=jest"
        //             powershell "C:/Python27/python.exe ./bin/xmlToJson.py output/coverage/jest/cobertura-coverage.xml --type=cobertura"
        //             powershell "C:/Python27/python.exe ./bin/xmlToJson.py output/coverage/jest/jest-junit.xml --type=jest"
        //         } 
        //         catch (Exception e){
        //             echo "exception while parsing xml coverage : ${e}"
        //             throw e
        //         }
        //     }
        // }
        // stage('Generate Comparison Metrics'){
        //     if(fileExists('pr-coverage-report.json') && fileExists('master-coverage-report.json')) {
        //         try {
        //             result = powershell (script: "C:/Python27/python.exe ./bin/prComparisonMetrics.py master-coverage-report.json pr-coverage-report.json", returnStdout: true)
        //             pullRequest.comment(result)
        //         }
        //         catch(Exception e){
        //             echo "Unable to generate comparison metrics: ${e}"
        //             throw e
        //         }
        //     }
        // }
        stage ('Trigger e2e job or remote job') {
            // withCredentials([
            //     string(credentialsId: 'REMOTE_TOKEN', variable: 'REMOTE_TOKEN')
            // ]) {
            //     if (env.CHANGE_ID == null) {
            //     echo "triggering e2e scan"
            //     trigger_external_job('prod')
            //     } else {
            //         echo REMOTE_TOKEN.getClass()
            //         def handle = triggerRemoteJob abortTriggeredJob: true, 
            //                     auth: TokenAuth(apiToken: REMOTE_TOKEN, userName: 'tilsharm'),
            //                     job: 'https://sqbu-jenkins.wbx2.com/service07/job/team/job/online-buy-client/job/test-jobs/job/test_remote',
            //                     shouldNotFailBuild: true,
            //                     blockBuildUntilComplete : false
                                
            //         echo handle.getBuildStatus().toString();
            //     }   
            // }

            withCredentials([usernamePassword(credentialsId: 'JENKINS_CRED', passwordVariable: 'pwd', usernameVariable: 'user')]) {
                def handle = triggerRemoteJob abortTriggeredJob: true, 
                                auth: CredentialsAuth(credentials: 'JENKINS_CRED'),
                                job: 'https://sqbu-jenkins.wbx2.com/service07/job/team/job/online-buy-client/job/test-jobs/job/test_remote',
                                shouldNotFailBuild: true,
                                blockBuildUntilComplete : false
            }

        }
        stage('Clean Workspace') {
            cleanWs notFailBuild: true
        }
    }
}

