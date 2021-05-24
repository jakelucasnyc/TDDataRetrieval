from auth import Auth

if __name__ == '__main__':

	auth = Auth()
	code = auth.getInitialAuthCodeAuto()
	accessToken = auth.getAccessTokenFromCode(code)
	auth.saveTokens(auth.accessToken, auth.refreshToken, auth.accessExpiresIn, auth.refreshExpiresIn, auth.currentTime)