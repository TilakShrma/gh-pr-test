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
        stage('Clean Workspace') {
            cleanWs notFailBuild: true
        }
    }
}

