jái creer un fichier idpcertificate.pem  j'ai copier le le certificat du metadata fourni par keycloack 
j'ai vérifier le certificat avec openssl x509 -in certs/idp-certificate.pem -text -nooutAJ  IOA23 U
|



    //If strict is True, then the Toolkit will reject unsigned 
    //or unencrypted messages if it expects them to be singned or encrypted

    //Enable debug mode (outputs errors)

    
    //Service Provider Data that we are deploying


    //Identifier of the SP entity (must be a URI)


            // Specifies info about where and how the <AuthnResponse> message MUST be
         // returned to the requester, in this case our SP.



         // URL Location where the <Response> from the IdP will be returned


                     // SAML protocol binding to be used when returning the <Response> 
            // message. SAML Toolkit supports this endpoint for the 
            // HTTP-POST binding only.



                    // Specifies info about where and how the <Logout Request/Response> message MUST be sent.


            // URL Location where the <LogoutRequest> from the IdP will be sent (IdP-initiated logout)


     // URL Location where the <LogoutResponse> from the IdP will sent (SP-initiated logout, reply) 
            // OPTIONAL: only specify if different from url parameter 
            //"responseUrl": "https://<sp_domain>/?sls", 
            // SAML protocol binding to be used when returning the <Response>
            // message. SAML Toolkit supports the HTTP-Redirect binding 
            // only for this endpoint.



 // Specifies the constraints on the name identifier to be used to 
        // represent the requested subject. 
        // Take a look on src/onelogin/saml2/constants.py to see the NameIdFormat that are supported.


// Usually X.509 cert and privateKey of the SP are provided by files placed at 
        // the certs folder. But we can also provide them with the following parameters



 // Identity Provider Data that we want connected with our SP.




  // Identifier of the IdP entity (must be a URI)



  // SSO endpoint info of the IdP. (Authentication Request protocol)



  // URL Target of the IdP where the Authentication Request Message 
            // will be sent.


    
      //SAML protocol binding to be used when returning the response


    

     //SLO endpoint info of the Idp




      //URL Location where the <> from the Idp will be sent (Idp-initiated logout)


      //Public certificate of the IdP