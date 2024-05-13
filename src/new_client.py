new_client_flux = {
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
    Name, Surname, email adress, Phone number, Postal code, If he is interested in a weekly or bi-weekly maintenance/cleaning, Number of hour per intervention and if he has a message for us.

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
            "[END_OF_CALL]" : "form_new_client",
        }
    },
    "form_new_client" : {
        "type" : "post_function_calling",
        "model_name" : "gpt-3.5-turbo-0125",
        "system_prompt" : """Extract information from the conversation and fill the form below""",
        "function_calling_name" : "form",
        "function_calling_prompt" : {
            "name": {
                "type": "string",
            },
            "surname": {
                "type": "string",
            },
            "email": {
                "type": "email",
            },
            "phone_number": {
                "type": "phone_number",
            },
            "postal_code": {
                "type": "postal_code",
            },
            "maintenance_frequency": {
                "type": "string",
                "enum": ["weekly", "bi-weekly"],
            },
            "number_of_hour_per_intervention": {
                "type": "string",
            },
            "message": {
                "type": "string",
            },
        },
        "save_to_call_variable" : True,
        "replacement_value" : {
            "maintenance_frequency" : {
                "weekly" : "Toutes les semaines",
                "bi-weekly" : "Toutes les deux semaines"
            },
        },
        "action" : {
            "[DEFAULT]" : "post_request",
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
            "item_meta[24]": "[[message]]",
            "item_meta[56]": "[[maintenance_frequency]]",
            "item_meta[58]": "[[number_of_hour_per_intervention]]",
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
}