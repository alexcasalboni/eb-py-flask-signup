# eb-py-flask-signup
This Python sample application uses the [Flask](http://flask.pocoo.org/) framework and [Bootstrap](http://getbootstrap.com/) to build a simple, scalable customer signup form that is deployed to [AWS Elastic Beanstalk](http://aws.amazon.com/elasticbeanstalk/). The application stores data in [Amazon DynamoDB](http://aws.amazon.com/dynamodb/) and publishes notifications to the [Amazon Simple Notification Service (SNS)](http://aws.amazon.com/sns/) when a customer fills out the form.

## Instructional Videos
This app includes a quick 3-part video series on YouTube that will walk you through deploying, using, and customizing the application in 10 minutes or less.

1. [Part 1: http://youtu.be/rsg4YI4mljg](http://youtu.be/rsg4YI4mljg)
2. [Part 2: http://youtu.be/IuwfVX52PV8](http://youtu.be/IuwfVX52PV8)
3. [Part 3: http://youtu.be/DrRr-JgdgzE](http://youtu.be/DrRr-JgdgzE)

## Flask Debugging
Similar to themes, you can control Flask debugging by toggling the FLASK_DEBUG env var from the [Elastic Beanstalk Management Console](https://console.aws.amazon.com/elasticbeanstalk).