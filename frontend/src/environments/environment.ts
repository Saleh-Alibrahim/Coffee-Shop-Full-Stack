/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://localhost:5000', // the running FLASK api server url
  auth0: {
    url: 'saleh-dev.eu', // the auth0 domain prefix
    audience: 'coffe', // the audience set for the auth0 app
    clientId: '1eWKC9lgJO7tiuoXHbm7K9XnbQSGaxDp', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:4200', // the base url of the running ionic application. 
  }
};
