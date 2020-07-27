require('mocha-sinon');

const test = require('firebase-functions-test')({
  databaseURL: "https://love-bank-testing.firebaseio.com",
  storageBucket: "love-bank-testing.appspot.com",
  projectId: "love-bank-testing",
}, 'test/love-bank-testing-firebase-adminsdk-8n07u-bacc63c070.json');
const myFunctions = require('../lib/index.js');
const fcm_functions = require('../lib/fcm.js');

const chai = require('chai');
const sinon = require('sinon');
const assert = chai.assert;
const expect = chai.expect;
//sinon.stub(console, 'log');

// task FCM test
// trigger on task create
const snap = test.firestore.makeDocumentSnapshot({ title: 'test_title', description: 'test_description', reward: 10, creator_id: '0Q03Iwu5kLOVM3p52fi7JkSHYZA3', receiver_id: '2HWP7OqvmIcm12TK4B7saeG5gYd2' }, 'tasks/testtaskdoc');
describe('Task Create', () => {

  beforeEach(function () {
    this.sinon.stub(console, 'log');
  });

  it('should test task created and send out FCM', () => {
    process.env['GCLOUD_PROJECT'] = 'love-bank-testing';
    const wrapped = test.wrap(fcm_functions.task_create_notify);
    wrapped(snap);
    expect(console.log.calledWith('Detected Task Creation!')).to.be.true;
  })
  
})

// trigger on task delete
describe('Task Delete', () => {

  beforeEach(function () {
    this.sinon.stub(console, 'log');
  });

  it('should test task created and send out FCM', () => {
    process.env['GCLOUD_PROJECT'] = 'love-bank-testing';
    const wrapped = test.wrap(fcm_functions.task_delete_notify);
    wrapped(snap);
    expect(console.log.calledWith('Detected Task Deletion!')).to.be.true;
  })

})

// trigger on task update - task rewards update
const beforeSnap = test.firestore.makeDocumentSnapshot({ title: 'test_title', description: 'test_description', reward: 10, creator_id: '0Q03Iwu5kLOVM3p52fi7JkSHYZA3', receiver_id: '2HWP7OqvmIcm12TK4B7saeG5gYd2' }, 'tasks/testtaskdoc');
const afterSnap_reward = test.firestore.makeDocumentSnapshot({ title: 'test_title', description: 'test_description', reward: 15, creator_id: '0Q03Iwu5kLOVM3p52fi7JkSHYZA3', receiver_id: '2HWP7OqvmIcm12TK4B7saeG5gYd2' }, 'tasks/testtaskdoc');
const afterSnap_description = test.firestore.makeDocumentSnapshot({ title: 'test_title', description: 'test_description_changed', reward: 10, creator_id: '0Q03Iwu5kLOVM3p52fi7JkSHYZA3', receiver_id: '2HWP7OqvmIcm12TK4B7saeG5gYd2' }, 'tasks/testtaskdoc');
describe('Task Update', () => {
  
  beforeEach(function () {
    this.sinon.stub(console, 'log');
  });

  it('should detect change in task reward and send FCM', () => {
    process.env['GCLOUD_PROJECT'] = 'love-bank-testing';
    const change = test.makeChange(beforeSnap, afterSnap_reward);
    const wrapped = test.wrap(fcm_functions.task_update_notify);
    wrapped(change);

    expect(console.log.calledWith('Task Reward Updated')).to.be.true;
    //expect(console.log.calledWith('Send to device with token:  cfdmsxUjREPJhCds9jelNK:APA91bFO8ltGqRttI6RkGyZNK6tGoAFG3hkQ6Hw2niHphWpXonYLyHJkTW0s-aaN7bJdrxj8nyhNC0hCDwOMddSudgWUfPjqqghY_bPKqWqco-ohhW_ORAUdBw_2hu5kJ7dU22Cn3Yg2')).to.be.true;
    //expect(console.log.calledWith('Send to device with token:  ewGlJbZLNkRSkDYzzjDVAe:APA91bFzW64Xk7Tyufr9YvmGiDEgIMJUXP_Sya3FHWfReJTSUgKcRcd41XrAIyreQtC_6AY3MX__djbMqvZP73C7aibIpuWCukod9fjZB7xk15tol9rLIVSlfAYb4OjNWlekSq6st7iY')).to.be.true;
  })

  it('should detect change in task description and send FCM', () => {
    process.env['GCLOUD_PROJECT'] = 'love-bank-testing';
    const change = test.makeChange(beforeSnap, afterSnap_description);
    const wrapped = test.wrap(fcm_functions.task_update_notify);
    wrapped(change);

    expect(console.log.calledWith('Task Description Updated')).to.be.true;
    //expect(console.log.calledWith('Send to device with token:  cfdmsxUjREPJhCds9jelNK:APA91bFO8ltGqRttI6RkGyZNK6tGoAFG3hkQ6Hw2niHphWpXonYLyHJkTW0s-aaN7bJdrxj8nyhNC0hCDwOMddSudgWUfPjqqghY_bPKqWqco-ohhW_ORAUdBw_2hu5kJ7dU22Cn3Yg2')).to.be.true;
    //expect(console.log.calledWith('Send to device with token:  ewGlJbZLNkRSkDYzzjDVAe:APA91bFzW64Xk7Tyufr9YvmGiDEgIMJUXP_Sya3FHWfReJTSUgKcRcd41XrAIyreQtC_6AY3MX__djbMqvZP73C7aibIpuWCukod9fjZB7xk15tol9rLIVSlfAYb4OjNWlekSq6st7iY')).to.be.true;
  })
});

// user FCM test
// trigger on user update - balance
const beforeUser = test.firestore.makeDocumentSnapshot({ title: 'test_title', description: 'test_description', reward: 10, creator_id: '0Q03Iwu5kLOVM3p52fi7JkSHYZA3', receiver_id: '2HWP7OqvmIcm12TK4B7saeG5gYd2' }, 'tasks/testtaskdoc');
const afterUser = test.firestore.makeDocumentSnapshot({ title: 'test_title', description: 'test_description', reward: 15, creator_id: '0Q03Iwu5kLOVM3p52fi7JkSHYZA3', receiver_id: '2HWP7OqvmIcm12TK4B7saeG5gYd2' }, 'tasks/testtaskdoc');
describe('User Update', () => {

})

// twilio Invite SMS test
// trigger on invite create - send to Twilio magic number +15005550006
describe('Inivite SMS Test', () => {

})

test.cleanup();