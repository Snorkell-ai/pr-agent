from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware import Middleware
from starlette_context.middleware import RawContextMiddleware

from pr_agent.servers.github_app import router

middleware = [Middleware(RawContextMiddleware)]
app = FastAPI(middleware=middleware)
app.include_router(router)

handler = Mangum(app, lifespan="off")


def serverless(event, context):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    Args:
        dictionary (dict): The processed files map.
    
    Returns:
        bool: True if successful, False otherwise.
        The return type is optional and may be specified at the beginning of
        the ``Returns`` section followed by a colon.
        The ``Returns`` section may span multiple lines and paragraphs.
        Following lines should be indented to match the first line.
        The ``Returns`` section supports any reStructuredText formatting,
        including literal blocks::
            
            {
            'param1': param1,
            'param2': param2
            }
    """
    return handler(event, context)
