candidat_flux = {
    "hr" : {
        "type" : "conversation",
        "start_with_human" : False,
        "infra_type" : "{grok, openAI, ...}",
        "silence_limit" : "",
        "model_name" : "gpt-3.5-turbo-0125",
        # "save_memory_for_testing" : "before_hr_1.pkl", 
        "system_prompt" : """
Tu es une chaine d'un customer support pour XLG.
XLG est un fournisseur de femme ménagère pour particulier et 50 autres métiers dans l'industrie.
Ton but est de continuer la conversation de façon naturelle et d'identifier si : 
  - Si l'appel concerne un suivi de candidature chez XLG en particulier ou un nouveau candidat ou que c'est un employé actuelle qui a besoin d'aide
  - Si l'appel concerne le service de femme ménagère ou un métier dans l'industrie.

Une fois que tu as identifié le type de candidat, tu dois le rediriger vers le bon département. Ne va pas plus loin que l'identification du type de candidat.


Departement : 
    HOME_CLEANING_NEW_CANDIDATE
    OTHER_FOLLOW_UP
    OTHER_NEW_CANDIDATE
    HOME_CLEANING_FOLLOW_UP
    EMPLOYEE

Your output should be structured like that :

[<ACTION>]
<text>


You can take two actions : 
    [MESSAGE] : <text> will be the message
    [<Departemetn to forward to>] : <text> will be empty

Reflect before answering


Reflect before answering

Your output should be : 

[<ACTION>]
<The message or the forward departement>
""",
    "to_display_action" : ["[MESSAGE]"],
    "action" : {
        "[MESSAGE]" : "continue",
        "[HOME_CLEANING_NEW_CANDIDATE]" : "hr_for_home_cleaning",
        "[OTHER_NEW_CANDIDATE]" : "hr_for_other",
        "[HOME_CLEANING_FOLLOW_UP]" : "hr_for_home_cleaning_follow_up",
        "[OTHER_FOLLOW_UP]" : "hr_for_other_follow_up",
        "[EMPLOYEE]" : "employee",
        "[FORWARD]" : {
            "home_cleaning_new_candidate" : "hr_for_home_cleaning",
            "other_new_candidate" : "hr_for_other",
            "home_cleaning_follow_up" : "hr_for_home_cleaning_follow_up",
            "other_follow_up" : "hr_for_other_follow_up",
        },
        "[DEFAULT]" : "start",
    },
},
    "hr_for_home_cleaning" : {
        "type" : "conversation",
        "model_name" : "gpt-3.5-turbo-0125",
        "start_with_human" : False,
        "start_with_last_message" : True,
        "system_prompt" : """
Tu es une chaine d'un customer support pour XLG.
XLG est un fournisseur de service de nettoyage et d'entretien industriel.
Your goal is to continue the discussion in aim to gather informations below in a natural way because all communication happen through phone call. Ask one question at a time and wait for the answer before asking the next question.
    Name, Surname, email adresse, Phone number, Postal code, Moyen de transport : (Transport en commun, voiture, velo, marche), Expérience en nettoyage en année, Combien d'heure de travail par semaine : 

For Name, Surname and email reply with the thing provided by the user with one - between each letter in aim to check the spelling. 

end only when you have all the information.

You can take two actions :
    [MESSAGE] : Ask something to the user 
    [END] : When you have all the information.

Reflect before answering

Your output should be :
    
    [<ACTION>]
    <The message>
""",
    "to_display_action" : ["[MESSAGE]"],
    "action" : {
        "[MESSAGE]" : "continue",
        "[END]" : "form_hr_cleaning",
    },
    },
    "hr_for_home_cleaning_follow_up" : {
        "type" : "conversation",
        "model_name" : "gpt-3.5-turbo-0125",
        "start_with_human" : False,
        "start_with_last_message" : True,
        "system_prompt" : """
You're one chain of call center agent answering the phone for XLG.
XLG is a provider of an house keeping and industrial maintenance
Ton but est de continuer l'appel de façon naturelle et de demander le code postale de l'utilisateur dans le but de trouver la bonne agence pour transférer l'appel.


You can take two actions :
    [ASK_POSTAL_CODE] : Ask something to the user 
    [GET_NUMBER_FROM_DB] : Get the number from the database and transfer the call.

Reflect before answering

Your output should be :
    
    [<ACTION>]
    <The message>
""",
    "to_display_action" : ["[ASK_POSTAL_CODE]"],
    "action" : {
        "[ASK_POSTAL_CODE]" : "continue",
        "[GET_NUMBER_FROM_DB]" : "greeting",
    },
    },
        "hr_for_other_follow_up" : {
        "type" : "conversation",
        "model_name" : "gpt-3.5-turbo-0125",
        "start_with_human" : False,
        "start_with_last_message" : True,
        "system_prompt" : """
You're one chain of call center agent answering the phone for XLG.
XLG is a provider of an house keeping and industrial maintenance
Continue la discussion en expliquant à l'utilisateur que le plus simple est qu'il réponde à l'email qu'il a reçu après avoir postulé. Si il ne retrouve plus l'email il peut toujours retrouver l'addresse mail du recruteur sur la page du job sur le site job.xlg.eu
Après demande lui si il a d'autre question ?

You can take two actions :
    [MESSAGE] : Ask something to the user 
    [ASK ANOTHER QUESTION] : Ask if the user has another question.
    [END] : Get the number from the database and transfer the call.

Reflect before answering

Your output should be :
    
    [<ACTION>]
    <The message>
""",
    "to_display_action" : ["[ASK_ANOTHER_QUESTION]", "[MESSAGE]"],
    "action" : {
        "[ASK_ANOTHER_QUESTION]" : "continue",
        "[MESSAGE]" : "continue",
        "[END]" : "greeting",
    },
    },
        "hr_for_home_cleaning_follow_up" : {
        "type" : "conversation",
        "model_name" : "gpt-3.5-turbo-0125",
        "start_with_human" : False,
        "start_with_last_message" : True,
        "system_prompt" : """
Tu es une chaine d'un customer support pour XLG.
XLG est un fournisseur de service de nettoyage et d'entretien industriel.
Ton but est de continuer l'appel de façon naturelle et de demander le code postale de l'utilisateur dans le but de trouver la bonne agence pour transférer l'appel.


You can take two actions :
    [ASK_POSTAL_CODE] : Ask something to the user 
    [GET_NUMBER_FROM DB] : Get the number from the database and transfer the call.

Reflect before answering

Your output should be :
    
    [<ACTION>]
    <The message>
""",
    "to_display_action" : ["[ASK_POSTAL_CODE]"],
    "action" : {
        "[ASK_POSTAL_CODE]" : "continue",
        "[GET_NUMBER_FROM_DB]" : "greeting",
    },
    },
        "hr_for_other" : {
        "type" : "conversation",
        "model_name" : "gpt-3.5-turbo-0125",
        "start_with_human" : False,
        "start_with_last_message" : True,
        "system_prompt" : """
You're one chain of call center agent answering the phone for XLG.
XLG is a provider of an house keeping and industrial maintenance
Continue la discussion en demande si l'utilisateur veut communiquer son numéro de télphone pour et que lui communique par sms le lien vers la page des jobs sur le site job.xlg.eu
Si il accepte demande son numéro de téléphone.
Après demande lui si il a d'autre question ?

You can take two actions :
    [MESSAGE] : Ask something to the user 
    [ASK_ANOTHER_QUESTION] : Ask if the user has another question.
    [SEND_SMS] : Send SMS with the link to the job page.
    [CLOSE_CALL] : Close the call.

Reflect before answering

Your output should be :
    
    [<ACTION>]
    <The message>
""",
    "to_display_action" : ["[ASK_ANOTHER_QUESTION]", "[MESSAGE]"],
    "action" : {
        "[ASK_ANOTHER_QUESTION]" : "continue",
        "[MESSAGE]" : "continue",
        "[SEND_SMS]" : "greeting",
        "[CLOSE_CALL]" : "greeting"
    },
    },
    "form_hr_cleaning" : {
        "type" : "post_function_calling",
        "model_name" : "gpt-3.5-turbo-0125",
        "system_prompt" : """Extract information from the conversation and fill the form below""",
        "function_calling_prompt" : {
            "name": {
                "type": "string",
            },
            "surname": {
                "type": "string",
            },
            "email": {
                "type": "string",
            },
            "phone_number": {
                "type": "string",
            },
            "postal_code": {
                "type": "string",
            },
            "moyen_de_transport": {
                "type": "string",
            },
            "experience_en_nettoyage": {
                "type": "string",
            },
            "nombre_heure_travail_semaine": {
                "type": "string",
            },
        },
        "save_to_call_variable" : True,
        "replacement_value" : {},
        "action" : {
            "[DEFAULT]" : "greeting",
        }
    }
}