pipeline{
    agent none
    timestamps {
        stage('Checkout Git Repo') {
            git credentialsId: 'fe4effdc-f62d-4624-bcc7-d4749675f873',
            branch: 'master',
            url: 'https://github.com/TilakShrma/gh-pr-test.git'
        }
        stage('Test') {
            echo "test stage"
        }
        stage('Clean Workspace') {
            cleanWs notFailBuild: true
        }
}
}
