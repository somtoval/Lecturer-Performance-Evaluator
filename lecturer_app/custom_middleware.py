class RailwayCorsFix:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        # Add a header that's sometimes needed for Railway specifically
        response["Cross-Origin-Resource-Policy"] = "cross-origin"
        return response