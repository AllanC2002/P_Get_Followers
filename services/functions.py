from models.models import Followers, Profile
from conections.mysql import conection_userprofile

def get_followers(user_id):
    session = conection_userprofile()

    # Verify account active follow (status)
    profile = session.query(Profile).filter_by(Id_User=user_id, Status_account=1).first()
    if not profile:
        session.close()
        return {"error": "Profile not found or inactive"}, 404

    # Search followers
    followers = (
        session.query(Profile)
        .join(Followers, Followers.Id_Follower == Profile.Id_User)
        .filter(Followers.Id_Following == user_id, Followers.Status == 1)
        .all()
    )

    # Dict
    result = [{
        "Id_User": follower.Id_User,
        "User_mail": follower.User_mail,
        "Name": follower.Name,
        "Lastname": follower.Lastname
    } for follower in followers]

    session.close()
    return {"followers": result}, 200
