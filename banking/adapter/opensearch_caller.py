from miniagent import configure
from miniagent.adapter import Adapter
from opensearchpy import OpenSearch, exceptions
from miniagent.flask_zipkin import child_zipkin_span
from typing import Callable

class OpensearchCaller(Adapter):

    client = None

    def call_get(self, url: str, index: str, query: dict = {}, parser: Callable[[dict], dict]=None) -> tuple[int, dict]:

        with child_zipkin_span('opensearch.index='+index) as span:
            header = dict(
                        trace_id = span.zipkin_attrs.trace_id,
                        span_id = span.zipkin_attrs.span_id,
                        parent_span_id = span.zipkin_attrs.parent_span_id,
                        flags = span.zipkin_attrs.flags,
                        is_sampled = span.zipkin_attrs.is_sampled
                    )
            
            span.update_tags(
                query=query
            )

            try:
                self.client = OpenSearch(
                    hosts = url,
                    http_compress = True, # enables gzip compression for request bodies
                )
                
            except exceptions.ConnectionError as e:
                return -1, {"message":"ConnectionError to {}".format(url)}

            response = self.client.search(
                            body = query,
                            index = index
                        )
            
            result = response.copy()

            if parser:
                result = parser(result)

            span.update_tags(
                result=result
            )

        return 1, result

    def __del__(self):
        try:
            self.client.close()
        except Exception as e:
            pass

    def get_status(self) -> int:
        return 1