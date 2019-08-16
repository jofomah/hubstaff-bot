#!/usr/bin/env /bin/sh

set -e

function display_help {
    echo """
    Available commands
    ----------------------------------------------------------------------------
    gen_auth_token     : generate HubStaff API auth token

    test_py_lint       : run flake8 tests

    setup              : creates models' database tables

    shell              : run sh

    start_dev          : start Flask server for development

    test_py            : run Flask app python code test cases, lint check and test coverage
    """
}

function generate_auth_token {
    python generate_auth_token.py
}

function setup {
    # create model tables
    python db_create.py
}

function check_lint {
    flake8
}

function test_coverage {
    pytest --cov=hubstaff --cov-config=.coveragerc hubstaff/tests/

    echo "Nice Job!!!"
}

case "$1" in
    gen_auth_token )
        generate_auth_token
    ;;

    help )
        display_help
    ;;
    
    setup )
        setup
    ;;

    shell )
        sh
    ;;

    start_dev )
        # ensure that FLASK_ENV is "development"
        export FLASK_ENV=development

        setup
        python run.py
    ;;

    test_py )
        # ensure that FLASK_ENV is "testing"
        export FLASK_ENV=testing

        setup
        check_lint
        test_coverage
    ;;

    test_py_lint )
        check_lint
    ;;

    * )
        display_help
    ;;
esac
