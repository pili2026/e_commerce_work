import inspect
import traceback
from typing import Any

from graphql import GraphQLError, GraphQLResolveInfo
from pydantic import ValidationError
from strawberry.extensions import SchemaExtension

from util.app_error import AppError, ErrorCode


class APIErrorHandler(SchemaExtension):

    async def resolve(self, _next: callable, root: Any, info: GraphQLResolveInfo, *args, **kwargs):
        try:
            result = _next(root, info, *args, **kwargs)

            if inspect.isawaitable(result):
                result = await result

            return result
        except AppError as e:
            extension = self.__make_error_extension(e.code, e)

            return GraphQLError(
                message=e.message,
                extensions=extension,
            )
        except ValidationError as e:
            err_msg = self.__make_validation_error_message(e)
            extensions = self.__make_error_extension(ErrorCode.INVALID_FORMAT, e)

            return GraphQLError(
                message=err_msg,
                extensions=extensions,
            )
        except Exception as e:
            err_msg = "Internal server error."
            extensions = self.__make_error_extension(ErrorCode.SERVER_ERROR, e)

            return GraphQLError(
                message=err_msg,
                extensions=extensions,
            )

    def __make_error_extension(self, code: ErrorCode, e: Exception):
        debug_info = {
            "exception_type": type(e).__name__,
            "message": str(e),
            "stack_trace": traceback.format_exc(),
        }

        extensions = {
            "code": code.value,
            "debug_info": debug_info,
        }

        return extensions

    def __make_validation_error_message(self, e: ValidationError):
        formatted_pydantic_err_msg_list = []

        for err in e.errors():
            pydantic_err_field = ".".join(map(str, err["loc"]))
            pydantic_err_type = err["type"]
            pydantic_err_msg = err["msg"]
            formatted_err_msg = f"{pydantic_err_field}: {pydantic_err_type}, {pydantic_err_msg}"
            formatted_pydantic_err_msg_list.append(formatted_err_msg)

        all_validation_error_message = "; ".join(formatted_pydantic_err_msg_list)
        return all_validation_error_message
