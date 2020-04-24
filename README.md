# ankipo
This addon let's you add audio from (aws) polly to your deck.

[Ankiweb(2090845100)](https://ankiweb.net/shared/info/2090845100)

## config
```json
{
  "access_id": "",
  "access_key": "",
  "audio_field": "audio",
  "engine": "standard",
  "query_fields": ["text"],
  "query_fields_seperator": "<break/>",
  "template": "{text}",
  "region": "eu-west-1",
  "voice": ""
}
```

- **access_id**: The id (NOT YOUR LOGIN CREDENTIAL) of the aws account you want to use.
- **access_key**: The key (NOT THE PASSWORD) for the aws account you want to use.
- **audio_field**: The name of the audio field you want to save the audio reference to.
- **engine**: The name of the engine you want to use (standard or neural).
- **query_fields**: A list of fields you want the audio from.
- **query_fields_seperator**: The seperator that will be used to combine those fields.
- **template**: The template you can use to supply some ssml decorators. You can also use **{combined}** or single field names as a reference like **{field1}**, **{field2}**. The have to be in the **query_fields** list tho.
- **region**: The region of your aws instance.
- **voice**: The aws polly voice you want to use.

### example

If I would want to create a audio file from the fields **singular1** and **singular2**, which
contain the first and second conjugated forms of some german verb,
seperated by a short break of 1s and save the result to the **audio** field,
I would do it like this:

```json
{
  "access_id": "idididididididid",
  "access_key": "keykeykeykeykey",
  "audio_field": "audio",
  "engine": "standard",
  "query_fields": ["singular1", "singular2"],
  "query_fields_seperator": "<break time=\"1s\">",
  "template": "{combined}",
  "region": "eu-west-1",
  "voice": "Hans"
}
```

you could also change the template to this (same result):

```json
{
"template": "{singular1}<break time=\"1s\">{singular2}"
}
```

or this (same result):

```json
{
"template": "<speak>{singular1}<break time=\"1s\">{singular2}</speak>"
}
```

