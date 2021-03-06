using System;
using System.Collections;
using System.Reflection;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

/// <summary>
/// This class handles all the network requests and serialization/deserialization of data
/// </summary>
public class NetworkManager : MonoBehaviour {

    // reference to BotUI class
    public BotUI botUI;
    
    // the url at which bot's custom connector is hosted
    private const string app_url = "https://miika-virtual-partner.herokuapp.com/chatbot";
	
	[Serializable]
    public class Message
    {
        public string sender;
        public string messages;
        
    }

    /// <summary>
    /// This method is called when user has entered their message and hits the send button.
    /// </summary>
    public void SendMessageToBackend () {
        // get user messasge from input field, create a json object 
        // from user message and then clear input field
        string messageFromInput = botUI.input.text;
        botUI.input.text = "";

		PostMessage msg = new PostMessage {
            sender = "user",
            message = messageFromInput
        };
		
		
        
        string jsonBody = JsonUtility.ToJson(msg);

        // update UI object with user message
        botUI.UpdateDisplay("user", messageFromInput, "text");

        // Create a post request with the data to send to Rasa server
        StartCoroutine(PostRequest(app_url, jsonBody));
    }

    /// <summary>
    /// This is a coroutine to asynchronously send a POST request to the Rasa server with 
    /// the user message. The response is deserialized and rendered on the UI object.
    /// </summary>
    
    IEnumerator PostRequest(string url, string json)
    {
        var uwr = new UnityWebRequest(url, "POST");
        byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);
        uwr.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
        uwr.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
        uwr.SetRequestHeader("Content-Type", "application/json");

        //Send the request then wait here until it returns
        yield return uwr.SendWebRequest();
		
		RecieveMessage(uwr.downloadHandler.text);
		
	}	


    /// <summary>
    /// This method updates the UI object with bot response
    /// </summary>
    /// <param name="response">response json recieved from the bot</param>
    public void RecieveMessage (string response) {
		
		
		
        // Deserialize response recieved from the bot
       

        // show message based on message type on UI
        
                // print data
		if (response != null ) {
		botUI.UpdateDisplay("bot", response, "text");
		
                }
				
            }
			
        
    

    /// <summary>
    /// This method gets url resource from link and applies it to the passed texture.
    /// </summary>
    /// <param name="url">url where the image resource is located</param>
    /// <param name="image">RawImage object on which the texture will be applied</param>
    /// <returns></returns>
    
}