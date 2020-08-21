require('dotenv').config(); // ENV file should be placed within functions folder

var AWS = require('aws-sdk');

// Using AWS Simple Notification Service
export function publish_sms(message, phone_number) {
  // Set region
  AWS.config.update({ region: 'us-east-1' });
  // Create publish parameters
  var params = {
    Message: message, /* required */
    PhoneNumber: phone_number,
    MessageAttributes: {
      'AWS.SNS.SMS.SMSType': {
        DataType: 'String',
        StringValue: 'Transactional'
      }
    }
  };
  // var sns = new AWS.SNS();
  // sns.publish(params, function(err, data) {
  //   if (err) console.log(err, err.stack); // an error occurred
  //   else     console.log(data);           // successful response
  // });

  // Create promise and SNS service object
  var publishTextPromise = new AWS.SNS({ apiVersion: '2010-03-31' }).publish(params).promise();

  // Handle promise's fulfilled/rejected states
  publishTextPromise.then(
    function (data) {
      console.log("MessageID is " + data.MessageId);
    }).catch(
      function (err) {
        console.log(err);
        console.error(err, err.stack);
      });

}


// Using AWS Simple Email Service
export function publish_email(title, content, email_address, source_email, reply_to_email) {
  // Set region
  AWS.config.update({ region: 'us-west-2' });
  // Create sendEmail params 
  var params = {
    Destination: { /* required */
      CcAddresses: [

      ],
      ToAddresses: [
        email_address,
      ]
    },
    Message: { /* required */
      Body: { /* required */
        Html: {
          Charset: "UTF-8",
          Data: "<body>" + content + "</body>"
        },
        Text: {
          Charset: "UTF-8",
          Data: "TEXT_FORMAT_BODY"
        }
      },
      Subject: {
        Charset: 'UTF-8',
        Data: title,
      }
    },
    Source: source_email, /* required */
    ReplyToAddresses: [
      reply_to_email,
      /* more items */
    ],
  };

  // Create the promise and SES service object
  var sendPromise = new AWS.SES({ apiVersion: '2010-12-01' }).sendEmail(params).promise();

  // Handle promise's fulfilled/rejected states
  sendPromise.then(
    function (data) {
      console.log(data.MessageId);
    }).catch(
      function (err) {
        console.error(err, err.stack);
      });
}


//Using AWS Simple Email Service with created templates
// export function publish_email_templated(content, email_adress, source_email, reply_to_email){
  
// }
