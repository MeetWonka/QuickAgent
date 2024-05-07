voice_bot = {
    "start" : {
        "type" : "conversation",
        "start_with_human" : False,
        "infra_type" : "{grok, openAI, ...}",
        "silence_limit" : "",
        "model_name" : "gpt-3.5-turbo-0125",
        "system_prompt" : """
You're one chain of call center agent answering the phone for XLG. 
XLG is a provider of an house keeping and industrial maintenance
Here are the instructions for handling a call.
Your goal will be to assess user need and forward to the right departement : 
    accountancy/provider : Every provider of XLG of question about accountancy
    new client : Every poeple that seems to want a service provided by XLG
    hr : Every poeple that want to become an employee at XLG (house keeper, worker, employee, ...)
    human : If client want to talk with an human or angry of speaking to a bot. Don't hesitate to forward to human
    other request : if in four messages you where not able to classify the request

You can take two actions : 
    [MESSAGE] : Ask something to the user 
    [FORWARD] : Output only the word for the departement to forward to call to. 

The conversation should go like that :
    Ask one opening question
    Have an implicit confirmation from the user for the departement to be transfered
    Forward once confirmed

Reflect before answering

Your output should be : 

[<ACTION>]
<The message or the forward departement>
""",
    "to_display_action" : ["[MESSAGE]"],
    "action" : {
        "[MESSAGE]" : "continue",
        "[FORWARD]" : {
            "hr" : "hr",
            "new client" : "new_client",
            "accountancy/provider" : "accountancy/provider",
            "human" : "human",
            "other request" : "other request",
        },
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
    Fill this from with the client : 
        Name : 
        Surname : 
    

You can take two actions : 
    [MESSAGE] : Ask something to the user 
    [END OF CALL] : Output your closing message

The conversation should be an normal conversation between an call center agent and the user

Reflect before answering

Your output should be : 

[<ACTION>]
<The message>
        """,
        "to_display_action" : ["[MESSAGE]"],
        "action" : {
            "[MESSAGE]" : "continue",
            "[END OF CALL]" : "form",
        }
    },
    "form" : {
        "type" : "post_function_calling",
        "model_name" : "gpt-3.5-turbo-0125",
        "system_prompt" : """
            Extract information from the conversation and fill the form below
        """,
        "function_calling_name" : "form",
        "function_calling_prompt" : {
            "name": {
                "type": "string",
            },
            "surname": {
                "type": "string",
            }
        },
        "save_to_call_variable" : True,
        "memory_key" : {
            "email" : "the_client_email",
            "name" : "the_client_name",
            "surname" : "the_client_surname",
            "postal_code" : "the_client_postal_code",#if not we don't use it
        },
        "option" : {
            "[DEFAULT]" : "",
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
        "data" : {
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
        "option" : {
            "[2xx]" : "greeting",
            "[3xx]" : "greeting",
            "[4xx]" : "greeting",
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
    }
}