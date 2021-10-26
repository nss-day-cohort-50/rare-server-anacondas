from http.server import BaseHTTPRequestHandler, HTTPServer
from categories import get_all_categories, get_single_category, create_category, delete_category, update_category
from posts import get_all_posts, get_single_post, create_post, delete_post, update_post
from tags import get_all_tags, get_single_tag, create_tag, delete_tag, update_tag
from comments import get_all_comments, get_single_comment, create_comment, delete_comment, update_comment
from users import get_all_users, get_single_user, create_user, delete_user, update_user
from reactions import get_all_reactions, get_single_reaction, create_reaction, delete_reaction, update_reaction
from subscriptions import get_all_subscriptions, get_single_subscription, create_subscription, delete_subscription, update_subscription
import json


class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]


        if "?" in resource:
           

            param = resource.split("?")[1]  
            resource = resource.split("?")[0]  
            pair = param.split("=") 
            key = pair[0]  
            value = pair[1]  

            return ( resource, key, value )

    
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  
            except ValueError:
                pass  

            return (resource, id)



   
    def _set_headers(self, status):
       
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

  
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

   
    def do_GET(self):
        self._set_headers(200)

        response = {}

        
        parsed = self.parse_url(self.path)

      
        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"
            elif resource == "comments":
                if id is not None:
                    response = f"{get_single_comment(id)}"
                else:
                    response = f"{get_all_comments()}"
            elif resource == "tags":
                if id is not None:
                    response = f"{get_single_tag(id)}"
                else:
                    response = f"{get_all_tags()}"
            elif resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"
            elif resource == "users":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = f"{get_all_users()}" 
            elif resource == "subscriptions":
                if id is not None:
                    response = f"{get_single_subscription(id)}"
                else:
                    response = f"{get_all_subscriptions()}" 

      
   

        self.wfile.write(response.encode())


        



   


    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        
        post_body = json.loads(post_body)

       
        (resource, id) = self.parse_url(self.path)

   
        new_category = None
        new_post = None
        new_tag = None
        new_comment = None
        new_subscription = None

       
        if resource == "categories":
            new_category = create_category(post_body)
            self.wfile.write(f"{new_category}".encode())
        if resource == "posts":
            new_post = create_post(post_body)
            self.wfile.write(f"{new_post}".encode())
        if resource == "comments":
            new_comment = create_comment(post_body)
            self.wfile.write(f"{new_comment}".encode())
        if resource == "tags":
            new_tag = create_tag(post_body)
            self.wfile.write(f"{new_tag}".encode())
        if resource == "subscriptions":
            new_tag = create_subscription(post_body)
            self.wfile.write(f"{new_subscription}".encode())



    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "categories":
            success = update_category(id, post_body)
        if resource == "tags":
            success = update_tag(id, post_body)
        if resource == "posts":
            success = update_post(id, post_body)
        if resource == "comments":
            success = update_comment(id, post_body)
        if resource == "users":
            success = update_user
            (id, post_body)
        if resource == "subscriptions":
            success = update_subscription
            (id, post_body)

        

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())



    def do_DELETE(self):
   
        self._set_headers(204)

   
        (resource, id) = self.parse_url(self.path)

  
        if resource == "categories":
            delete_category(id)
            self.wfile.write("".encode())
        if resource == "comments":
            delete_post(id)
            self.wfile.write("".encode())
        if resource == "posts":
            delete_tag(id)
            self.wfile.write("".encode())
        if resource == "tags":
            delete_comment(id)
            self.wfile.write("".encode())
        if resource == "subscriptions":
            delete_subscription(id)
            self.wfile.write("".encode())
 



def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
