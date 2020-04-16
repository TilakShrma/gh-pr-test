timestamps {
    node(label: 'master') {
        stage('Checkout Git Repo') {
            git credentialsId: 'fe4effdc-f62d-4624-bcc7-d4749675f873',
            branch: 'master',
            url: 'https://github.com/TilakShrma/gh-pr-test.git'
        }
        stage('Test stage') {
            echo "test stage in progress"
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
            if (env.BRANCH_NAME == 'master') {
            // steps {
            //     script {
            //         currentBuild.result = 'SUCCESS'
            //      }
            //     step([$class: 'MasterCoverageAction', scmVars: [GIT_URL: env.GIT_URL]])
            // }
            currentBuild.result = 'SUCCESS'
            step([$class: 'MasterCoverageAction', scmVars: [GIT_URL: env.GIT_URL]])
            }
            
        }
        stage('PR Coverage to Github') {
            //when { allOf {not { branch 'master' }; expression { return env.CHANGE_ID != null }} }
            if ( env.BRANCH_NAME != 'master' && (env.CHANGE_ID != null)) {
            // steps {
            //     script {
            //         currentBuild.result = 'SUCCESS'
            //      }
            //     step([$class: 'CompareCoverageAction', publishResultAs: 'statusCheck', scmVars: [GIT_URL: env.GIT_URL]])
            // }
            currentBuild.result = 'SUCCESS'
            step([$class: 'CompareCoverageAction', publishResultAs: 'statusCheck', scmVars: [GIT_URL: env.GIT_URL]])
        }
        }
        stage('Clean Workspace') {
            cleanWs notFailBuild: true
        }
    }
}

