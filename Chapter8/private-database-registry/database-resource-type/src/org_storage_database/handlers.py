import logging
from typing import Any, MutableMapping, Optional
from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
    exceptions,
    identifier_utils,
)

from .dbclient import DbClient
from .models import ResourceHandlerRequest, ResourceModel


# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Org::Storage::Database"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint

def get_db_connection_parameters(request: ResourceHandlerRequest) -> (str, str, str):
    return (
        request.desiredResourceState.RdsHost,
        request.desiredResourceState.RdsUser,
        request.desiredResourceState.RdsPassword
    )

def get_db_properties(request: ResourceHandlerRequest) -> (str, str, str):
    return (
        request.desiredResourceState.DatabaseName,
        request.desiredResourceState.DatabaseUser,
        request.desiredResourceState.DatabasePassword,
    )

def only_password_change(request: ResourceHandlerRequest) -> bool:
    if (
        request.desiredResourceState.DatabaseName == request.previousResourceState.DatabaseName and 
        request.desiredResourceState.DatabaseUser == request.previousResourceState.DatabaseUser
        ):
            return True



@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )

    host, rds_user, rds_pw = get_db_connection_parameters(request)
    db, user, pw = get_db_properties(request)
    
    client = DbClient(host, rds_user, rds_pw)
    if client.user_exists(user):
        LOG.error(f'User {user} already exists! Consider importing it to the stack')
        return ProgressEvent.failed(HandlerErrorCode.AlreadyExists, 
                                    f'User {user} already exists! Consider importing it to the stack')
    
    if client.db_exists(db):
        LOG.error(f'Database {db} already exists! Consider importing it to the stack')
        return ProgressEvent.failed(HandlerErrorCode.AlreadyExists, 
                                    f'Database {db} already exists! Consider importing it to the stack')
  
    try:
        client.create_or_update(db, user, pw)
        LOG.info('Database created')
        progress.status = OperationStatus.SUCCESS
    except Exception as e:
        LOG.error(f'Failed to create resource. Reason: {e}')
        return ProgressEvent.failed(HandlerErrorCode.HandlerInternalFailure, 
                                    f'Failed to create resource. Reason: {e}')
    
    return read_handler(session, request, callback_context)


@resource.handler(Action.UPDATE)
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
 
    host, rds_user, rds_pw = get_db_connection_parameters(request)
    db, user, pw = get_db_properties(request)
    client = DbClient(host, rds_user, rds_pw)
    
    if not client.db_exists(db):
        return ProgressEvent.failed(HandlerErrorCode.NotFound, 
                                    f'Database does not exist')

    if not client.user_exists(user):
        return ProgressEvent.failed(HandlerErrorCode.NotFound, 
                                    f'User does not exist')

    try:
        if only_password_change(request):
            client.change_user_password(user, pw)
        else:
            client.create_or_update(db, user, pw)
        progress.status = OperationStatus.SUCCESS
    except Exception as e:
        return ProgressEvent.failed(HandlerErrorCode.HandlerInternalFailure, 
                                    f'Failed to create resource. Reason: {e}')
        
    return read_handler(session, request, callback_context)


@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=None,
    )
    
    host, rds_user, rds_pw = get_db_connection_parameters(request)
    db, user, _ = get_db_properties(request)
    client = DbClient(host, rds_user, rds_pw)
    
    if not client.db_exists(db):
        return ProgressEvent.failed(HandlerErrorCode.NotFound, 
                                    f'Database {db} does not exist')

    if not client.user_exists(user):
        return ProgressEvent.failed(HandlerErrorCode.NotFound, 
                                    f'User {user} does not exist')

    try:
        client.delete(db, user)
        progress.status = OperationStatus.SUCCESS
    except Exception as e:
        return ProgressEvent.failed(HandlerErrorCode.HandlerInternalFailure, 
                                    f'Failed to delete resource. Reason: {e}')

    return progress


@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    
    host, rds_user, rds_pw = get_db_connection_parameters(request)
    db, user, pw = get_db_properties(request)
    client = DbClient(host, rds_user, rds_pw)

    if not client.db_exists(db):
        return ProgressEvent.failed(HandlerErrorCode.NotFound, 
                                    f'Database {db} does not exist')

    if not client.user_exists(user):
        return ProgressEvent.failed(HandlerErrorCode.NotFound, 
                                    f'User {user} does not exist')

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


@resource.handler(Action.LIST)
def list_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    host, rds_user, rds_pw = get_db_connection_parameters(request)
    db, user, _ = get_db_properties(request)
    client = DbClient(host, rds_user, rds_pw)
    
    models = []
    
    if client.db_exists(db) and client.user_exists(user):
        models.append(model)
        
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModels=models,
    )
