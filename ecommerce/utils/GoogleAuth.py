import requests
import json

class GoogleStrategy():
    
    def __init__(self, scope, access_type, redirect_uri, client_id, client_secret):
        self.scope = scope
        self.access_type = access_type
        self.response_type = 'code'
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret
        

    def authenticationLink(self):
        ref = f"https://accounts.google.com/o/oauth2/v2/auth?scope={self.scope}&access_type={self.access_type}&response_type={self.response_type}&redirect_uri={self.redirect_uri}&client_id={self.client_id}"
        return ref
    
    def completeAuth(self, authorizationCode):
        
        credentials = self.getCredentials(authorizationCode)
        profile = self.getProfile(credentials)
        return profile
    
    def getCredentials(self, authorizationCode):
        data = {'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': authorizationCode,
                'grant_type': 'authorization_code',
                'redirect_uri':self.redirect_uri}
        res = requests.post(url='https://oauth2.googleapis.com/token?', data=data)
        return json.loads(res.text)


    def getProfile(self, credentials):
        headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
        URL = 'https://www.googleapis.com/oauth2/v2/userinfo'
        rawProfile = requests.get(url=URL, headers=headers)
        profile = json.loads(rawProfile.text)
        return profile
    
class FacebookStrategy():
    
    def __init__(self, scope, redirect_uri, client_id, client_secret, state="abc123"):
        self.scope = scope
        self.response_type = 'code'
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.state = state

    def authenticationLink(self):
        ref = f"https://www.facebook.com/v6.0/dialog/oauth?client_id={self.client_id}&redirect_uri={self.redirect_uri}&state={self.state}"
        return ref
    
    def completeAuth(self, authorizationCode):
        credentials = self.getCredentials(authorizationCode)
        profile = self.getProfile(credentials)
        print("FacebookStrategy.completeAuth(self, authorizationCode):")
        print(profile)
        return profile
    
    def getCredentials(self, authorizationCode):
        params = {'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': authorizationCode,
                'redirect_uri':self.redirect_uri}
        res = requests.get(url='https://graph.facebook.com/v6.0/oauth/access_token?', params=params)
        return json.loads(res.text)


    def getProfile(self, credentials):
        params = { 'fields': 'id,email,name,gender,location,picture', 'access_token': credentials['access_token'] }
        URL = 'https://graph.facebook.com/me?'
        rawProfile = requests.get(url=URL, params=params)
        profile = json.loads(rawProfile.text)
        return profile
