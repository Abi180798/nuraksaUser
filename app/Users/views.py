"""Users view controol to serilize the users response endpoint to BaseResponse model.

All transaction from user router endpoint must request to this class.

"""


from .models import Users
from .schemas import UserModel, UserResponse, UsersResponse, ListMeta

class UserViews:

    def post(self, user : UserModel):
        response = UserResponse()
        response.badrequest()
        user = Users.addUser(user)
        if user is None:
            response.message = "username is has been used"
            return response
        response.data = user
        response.created()
        return response
    
    def get(self, limit, page):
        response = UsersResponse()
        response.data = Users.getUsers(limit, page)
        print(response.data)
        response.meta.totals = len(response.data)
        response.meta.limit = limit
        response.meta.curent_page = page
        response.meta.next_page = page + 1
        response.meta.previous_page = page -1
        return response
    
    def getSingle(self, id):
        response = UserResponse()
        response.notfound()
        user = Users.getUsersBy(Users.id_admin==id)
        if user is not None:
            response.data=user
            response.success()
        return response

    def update(self, user: UserModel,id):
        response = UserResponse()
        response.notfound()
        user = Users.update(user, id)
        if user is not None:
            response.data = user
            response.success()
        return response

    def delete(self, id):
        response = UserResponse()
        response.notfound()
        user = Users.delete(id)
        if user == True:
            response.success()
            response.message="success delete data"
        return response