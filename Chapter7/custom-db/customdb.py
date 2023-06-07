import requests
import json
import pymysql
import sys

SUCCESS = "SUCCESS"
FAILED = "FAILED"

class CustomResourceException(Exception):
    pass

def create_or_update_db(dbname, dbuser, dbpassword, rdsendpoint, rdsuser, rdspassword):
    create_db_query = f"CREATE DATABASE {dbname};"
    create_user_query = f"CREATE USER '{dbuser}'@'%' IDENTIFIED BY '{dbpassword}';"
    grant_query = f"GRANT ALL PRIVILEGES ON {dbname}.* TO '{dbuser}'@'%';"
    flush_query = "FLUSH PRIVILEGES;"
    try:
        conn = pymysql.connect(host=rdsendpoint,
                               user=rdsuser,
                               password=rdspassword)
        cursor = conn.cursor()
        cursor.execute(create_db_query)
        cursor.execute(create_user_query)
        cursor.execute(grant_query)
        cursor.execute(flush_query)
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as err:
        raise CustomResourceException(err)


def delete_db(dbname, dbuser, rdsendpoint, rdsuser, rdspassword):
    delete_db_query = f"DROP DATABASE {dbname}"
    delete_user_query = f"DROP USER '{dbuser}'"
    db_exists_query = f"SHOW DATABASES LIKE '{dbname}'"
    user_exists_query = f"SELECT user FROM mysql.user where user='{dbuser}'"
    try:
        conn = pymysql.connect(host=rdsendpoint,
                               user=rdsuser,
                               password=rdspassword)
        cursor = conn.cursor()
        if cursor.execute(db_exists_query):
            cursor.execute(delete_db_query)
        if cursor.execute(user_exists_query):
            cursor.execute(delete_user_query)
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as err:
        raise CustomResourceException(err)


def handler(event, context):
    input_props = event["ResourceProperties"]
    required_props = ["DBName", "RDSEndpoint", "RDSUser", "RDSPassword"]
    missing_props = [prop for prop in required_props if prop not in input_props]
    if missing_props:
        if event['RequestType'] == "Delete":
            send(event, context, SUCCESS, response_data={})
            sys.exit(0)
        reason = f"Required properties are missing: {missing_props}"
        send(event, context, FAILED, response_reason=reason, response_data={})
        raise CustomResourceException(reason)
    db_name = input_props["DBName"]
    rds_endpoint = input_props["RDSEndpoint"]
    rds_user = input_props["RDSUser"]
    rds_password = input_props["RDSPassword"]

    if "DBUser" not in input_props or len(input_props["DBUser"]) == 0:
        db_user = db_name
    else:
        db_user = input_props["DBUser"]

    if "DBPassword" not in input_props or len(input_props["DBPassword"]) == 0:
        db_password = db_name
    else:
        db_password = input_props["DBPassword"]

    try:
        if event["RequestType"] == "Delete":          
            delete_db(db_name, db_user, rds_endpoint, rds_user, rds_password)
        elif event["RequestType"] in ("Create", "Update"):
            create_or_update_db(db_name, db_user, db_password, rds_endpoint, rds_user, rds_password)
    except CustomResourceException as err:
        send(event, context, FAILED, responseReason=err, physicalResourceId="", responseData={})
        sys.exit(1)

    send(event, context, SUCCESS, physicalResourceId=db_name, responseData={})


def send(event, context, response_status, response_data, response_reason="", physical_resource_id=None, no_echo=False):
    response_url = event["ResponseURL"]

    print(response_url)

    response_body = {}
    response_body["Status"] = response_status
    response_body["Reason"] = response_reason
    response_body["PhysicalResourceId"] = physical_resource_id or context.log_stream_name
    response_body["StackId"] = event["StackId"]
    response_body["RequestId"] = event["RequestId"]
    response_body["LogicalResourceId"] = event["LogicalResourceId"]
    response_body["NoEcho"] = no_echo
    response_body["Data"] = response_data

    response_body = json.dumps(response_body)

    print(f"Response body:\n{response_body}")

    headers = {
        "content-type": "",
        "content-length": str(len(response_body))
    }

    try:
        response = requests.put(response_url,
                                data=response_body,
                                headers=headers)
        print(f"Status code: {response.reason}")
    except Exception as err:
        print(f"send(..) failed executing requests.put(..): {err}")
