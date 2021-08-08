from auth import Auth
import time
import logging

logger = logging.getLogger('firstLogin')
logging.basicConfig(level=logging.INFO)

def main():
    
    now = time.time()
    auth = Auth()
    code = auth.getInitialAuthCodeAuto()
    accessToken = auth.getAccessTokenFromCode(code)
    auth.saveTokens(auth.accessToken, auth.refreshToken, auth.accessExpiresIn, auth.refreshExpiresIn, auth.currentTime)
    
if __name__=='__main__':
    try:
        logger.info('Process starting...')
        main()
    except Exception as e:
        logger.exception(e)
    else:
        logger.info('Process complete')