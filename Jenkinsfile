def fullBranchUrl(branchName) { return "${scm.getUserRemoteConfigs()[0].getUrl()}/tree/$branchName" }

timestamps {
    node(label: 'master') {
        stage('Checkout Git Repo') {
            git credentialsId: 'fe4effdc-f62d-4624-bcc7-d4749675f873',
            branch: 'master',
            url: 'https://github.com/TilakShrma/gh-pr-test.git'
        }
        stage('Test stage') {
            echo "test stage in progress"
            echo "Branch name : ....${env.BRANCH_NAME}"
            echo "Change url : .....${env.CHANGE_URL}"
            echo "Change target: ....${env.CHANGE_TARGET}"
            echo "change branch: .....${env.CHANGE_BRANCH}"
            // sh 'npm install'
        }
        stage('Run tests') {
            // sh 'npm test'
        }
        stage('Archive and Record Tests') {
            if (fileExists('output/coverage/jest/cobertura-coverage.xml')) {
                archiveArtifacts 'output/coverage/jest/cobertura-coverage.xml'
                cobertura coberturaReportFile: 'output/coverage/jest/cobertura-coverage.xml'
            }
            else {
                echo 'XML report were not created'
            }
        }
        stage('Record Coverage') {
            if (env.CHANGE_ID == null) {
            currentBuild.result = 'SUCCESS'
            step([$class: 'MasterCoverageAction', scmVars: [GIT_URL: fullBranchUrl(env.BRANCH_NAME)]])
            } 
            else if (env.CHANGE_ID != null) {
            currentBuild.result = 'SUCCESS'
            step([$class: 'CompareCoverageAction', publishResultAs: 'statusCheck', scmVars: [GIT_URL: fullBranchUrl(env.CHANGE_BRANCH)]])
        }
            
        }
        stage('PR Coverage to Github') {
            
        }
        stage('Clean Workspace') {
            cleanWs notFailBuild: true
        }
    }
}

