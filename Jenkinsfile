pipeline{
    agent none
    stages {
        stage('Checkout Git Repo') {
            steps {
            git credentialsId: 'fe4effdc-f62d-4624-bcc7-d4749675f873',
            branch: 'master',
            url: 'https://github.com/TilakShrma/gh-pr-test.git'
            }
        }
        stage('Test') {
            steps {
            echo "test stage"
            }
        }
        stage('Clean Workspace') {
            steps {
            cleanWs notFailBuild: true
        }
        }
}
}
