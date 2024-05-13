from candidat import candidat_flux
from client import client_flux
from provider import provider_flux
from employee import employee_flux 
from other import other_flux

voice_bot = {
    "start" : {
        "type" : "conversation",
        "start_with_human" : False,
        "infra_type" : "{grok, openAI, ...}",
        "silence_limit" : "",
        "model_name" : "gpt-3.5-turbo-0125",
        "system_prompt" : """
Tu es une chaine d'un customer support pour XLG.
XLG est un fournisseur de service de nettoyage et d'entretien industriel.
Ton but est d'acceuillir le client et de le rediriger vers le bon departement : 
    CURRENT_CLIENT : Every current client that want to talk with XLG
    NEW_CLIENT : Every poeple that seems to want a service provided by XLG
    HR : Every poeple that want to become an employee at XLG (house keeper, worker, employee, ...)
    PROVIDER : Every provider of XLG or some poeple trying to propose service for XLG
    EMPLOYEE : Every employee/subcontractor of XLG that need to talk with someone
    HUMAN : If client want to talk with an human or angry of speaking to a bot. Don't hesitate to forward to human
    OTHER : if in four messages you where not able to classify the request

Ton message doit être structuré comme suit:

[<ACTION>]
<text>

Où tu peux prendre deux actions : 
    [WELCOME_MESSAGE] : <text> sera le message
    [<Departemetn to forward to>] : <text> sera vide

Refléchi avant de répondre
""",
    "to_display_action" : ["[MESSAGE]", "[WELCOME_MESSAGE]"],
    "action" : {
        "[WELCOME_MESSAGE]" : "continue",
        "[MESSAGE]" : "continue",
        "[HR]" : "hr",
        "[PROVIDER]" : "provider",
        "[CURRENT_CLIENT]" : "current_client",
        "[NEW_CLIENT]" : "new_client",
        "[EMPLOYEE]" : "employee",
        "[OTHER]" : "other",
        "[DEFAULT]" : "start",
    },
    },
    "new_client" : {
        "type" : "conversation",
        "model_name" : "gpt-3.5-turbo-0125",
        "start_with_human" : False,
        "start_with_last_message" : True,
        "system_prompt" : """
You're one chain of call center agent answering the phone for XLG. You work in the new client departement. 
XLG is a provider of an house keeping and industrial maintenance
Here are the instructions for handling a call.
Your goal is :
Check if client is interested in home maintenance, industial maintenance
Your goal is to continue the discussion in aim to gather informations below in a natural way because all communication happen through phone call. Ask one question at a time and wait for the answer before asking the next question.
    Name, Surname, email adress, Phone number, Postal code, If he is interested in a weekly or bi-weekly maintenance/cleaning, Number of hour per intervention

For Name, Surname and email reply with the thing provided by the user with one - between each letter in aim to check the spelling. 

Once you have all the information output [END_OF_CALL]
    

You can take two actions : 
    [MESSAGE] : Ask something to the user 
    [END_OF_CALL] : Output your closing message

The conversation should be an normal conversation between an call center agent and the user

Reflect before answering

Your output should be : 

[<ACTION>]
<The message>
        """,
        "to_display_action" : ["[MESSAGE]"],
        "action" : {
            "[MESSAGE]" : "continue",
            "[END_OF_CALL]" : "form",
        }
    },
    "greeting" : {
        "type" : "conversation",
        "model_name" : "gpt-3.5-turbo-0125",
        "start_with_human" : False,
        "start_with_last_message" : True,
        "save_memory_for_testing" : "before_greeting_1.pkl", 
        "system_prompt" : """
You're the last chain of call center agent answering the phone for XLG. 
XLG is a provider of an house keeping and industrial maintenance
Your goal is to continue the conversation in aim to gather the user experience and ask for a quotation for the service support. 
Thanks user for the action he ask during the call and ask user if he need more help
Present that for improvement you would like to to ask in a 1-5 scale the user satisfaction regarding the call. 
Once you have the information you can save notation
    

Do these three actions in three different messages, you can not output two actions at the same time: 
    1 - [ASK_USER] : Ask user if he have question left
    2 - [ASK_NOTATION] : Ask notation to user
    3 - [SAY_GOODBYE] : Say goodbye

The conversation should be an normal conversation between an call center agent and the user

Reflect before answering

Your output should be : 

[<ACTION>]
<The message>
        """,
        "to_display_action" : [["MESSAGE"],"[ASK_NOTATION]", "[ASK_USER]", "[SAY_GOODBYE]"],
        "action" : {
            "[MESSAGE]" : "continue",
            "[ASK_NOTATION]" : "continue",
            "[ASK_USER]" : "continue",
            "[SAY_GOODBYE]" : "form_end_of_call",
        }
    },
    "form_end_of_call" : {
        "type" : "post_function_calling",
        "model_name" : "gpt-3.5-turbo-0125",
        "system_prompt" : """Extract information from the conversation and fill the form below""",
        "function_calling_name" : "form",
        "function_calling_prompt" : {
            "satisfaction": {
                "type": "number",
                "enum": ["1", "2", "3", "4", "5"]
            },
        },
        "save_to_call_variable" : True,
        "replacement_value" : {},
        "action" : {
            "[DEFAULT]" : "finish",
        }
    },
    "post_request" : {
        "type" : "request",
        "url" : "https://home.xlg.eu/wp-admin/admin-ajax.php?lang=fr",  
        "method" : "POST",
        "header" : {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://home.xlg.eu",
            "referer": "https://home.xlg.eu/fr/titres-services-clients/",
            "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        },
        "body" : {
            "frm_action": "create",
            "form_id": "2",
            "frm_hide_fields_2": "%5B%22frm_field_74_container%22%2C%22frm_field_75_container%22%5D",
            "form_key": "vouscherchezuneaidemnagre2",
            "item_meta[0]": "",
            "frm_submit_entry_2": "f77302bdfc",
            "_wp_http_referer": "%2Ffr%2Ftitres-services-clients%2F",
            "item_meta[69]": "home.xlg.eu%2Ffr%2Ftitres-services-clients%2F",
            "item_meta[6]": "[[name]]",
            "item_meta[7]": "[[surname]]",
            "item_meta[8]": "[[phone_number]]",
            "item_meta[9]": "[[email]]",
            "item_meta[11]": "[[postal_code]]",
            "item_meta[24]": "[[maintenance_type]]",
            "item_meta[56]": "[[maintenance_frequency]]",
            "item_meta[58]": "[[hour_per_intervention]]",
            "item_meta[73]": "Non",
            "item_meta[75]": "",
            "item_meta[34][]": "Option+1",
            "item_meta[27]": "fr",
            "item_meta[32]": "",
            "item_meta[33]": "",
            "item_meta[63]": "",
            "item_meta[52]": "",
            "item_key": "",
            "frm__654bb1c63c174": "",
            "frm_state": "KcvUknayoo36IIMVtPpFUEoPSp0VMSOhq0OhBEajZzL0TaKhXdSnDDNRbV9MOkyf%2FbsKP0Y3srJfYmu5uesbC1cO6JfCqC63%2FcPuMWATsgvTqGdfJsH0%2FHNCgAp6Teqv",
            "action": "frm_entries_create",
            "nonce": "1e51e2bac3"
        },
        "action" : {
            "2xx" : "greeting",
            "3xx" : "greeting",
            "4xx" : "greeting",
        },
    },
    "get_agency_contact" : {
        "type" : "get_agency_phone_number_per_postal_code",
        "args" : {
            "postal_code" : "[[postal_code]]"
        },
        "output" : "phone_number",
        "option" : {
            "[FIND]" : "transfer_call",
            "[CLOSED]" : "greeting",
            "[HOLIDAY]" : "greeting",
            "[NOT_FOUND]" : "greeting",
        }
    },
    "get_urgent_contact" : {
        "type" : "get_urgent_phone_number",
        "output" : "phone_number",
        "option" : {
            "[FIND]" : "transfer_call",
            "[CLOSED]" : "greeting",
            "[HOLIDAY]" : "greeting",
            "[NOT_FOUND]" : "greeting",
        }
    },
    "send_sms" : {
        "type" : "sms",
        "phone_number" : "[[phone_number]]",
        "message" : "Bonjour, nous avons bien reçu votre demande, nous vous contacterons dans les plus brefs délais",
        "option" : {
            "[SUCCESS]" : "greeting",
            "[ERROR]" : "greeting",
        }
    },
    "transfer_call" : {
        "type" : "phone_transfer",
        "phone_number" : "[[phone_number]]",
        "option" : {
            "[SUCCESS]" : "end_call",
            "[AFTER_4_SONNERIE]" : "no_reply",
        }
    },
    "send_email" : {
        "type" : "send_email",
        "args" : {
            "email" : "[[email]]",
            "subject" : "Demande de devis",
        },
        "subject" : "Demande de devis",
    },
    **candidat_flux,
    **client_flux,
    **provider_flux,
    **employee_flux,
    **other_flux
}