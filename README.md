# Mastering AWS CloudFormation Second Edition

<a href="https://www.packtpub.com/product/mastering-aws-cloudformation-second-edition/9781805123903?utm_source=github&utm_medium=repository&utm_campaign="><img src="https://content.packt.com/B20999/cover_image_small.jpg" alt="Mastering AWS CloudFormation Second Edition" height="256px" align="right"></a>

This is the code repository for [Mastering AWS CloudFormation Second Edition](https://www.packtpub.com/product/mastering-aws-cloudformation-second-edition/9781805123903?utm_source=github&utm_medium=repository&utm_campaign=), published by Packt.

**Build resilient and production-ready infrastructure in Amazon Web Services with CloudFormation**

## What is this book about?
Mastering CloudFormation covers all the features that an engineer needs to use to effectively build, maintain, and operate large-scale infrastructures within AWS. It covers all the core features as well as various methods to successfully extend its capabilities beyond AWS.

This book covers the following exciting features:
* Understand modern approaches to IaC
* Develop universal, modular, and reusable CloudFormation templates
* Discover ways of applying continuous delivery with CloudFormation
* Implement IaC best practices in the AWS cloud
* Provision massive applications across multiple regions and accounts
* Automate template generation and software provisioning for AWS
* Extend CloudFormation features with custom resources and the registry
* Modularize and unify templates using modules and macros

If you feel this book is for you, get your [copy](https://www.amazon.com/dp/1805123904) today!

<a href="https://www.packtpub.com/?utm_source=github&utm_medium=banner&utm_campaign=GitHubBanner"><img src="https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png" 
alt="https://www.packtpub.com/" border="5" /></a>

## Instructions and Navigations
All of the code is organized into folders. For example, Chapter05.

The code will look like the following:
```
import boto3
def check_if_key_exists():
    client = boto3.client(<ec2>)
    try:
        resp = client.describe_key_pairs(KeyNames=[«mykey»])
    except Exception:
```

**Following is what you need for this book:**
If you are a developer who wants to learn how to write templates, a DevOps engineer or SRE interested in deployment and orchestration, or a solutions architect looking to understand the benefits of streamlined and scalable infrastructure management, this book is for you. Prior understanding of the AWS Cloud is necessary.

With the following software and hardware list you can run all code files present in the book (Chapter 1-12).
### Software and Hardware List
| Chapter | Software required | OS required |
| -------- | ------------------------------------ | ----------------------------------- |
| 1-12 | AWS CLI 1.18 or later | Mac OS X, and Linux (Any) |
| 1-12 | Python 3.6 or later | Windows, Mac OS X, and Linux (Any) |
| 1-12 | Homebrew 2.2 or later | Windows, Mac OS X, and Linux (Any) |
| 1-12 | Docker 19.03.5 or later | Windows, Mac OS X, and Linux (Any) |


### Related products
* AWS for Solutions Architects - Second Edition [[Packt]](https://www.packtpub.com/product/aws-for-solutions-architects-second-edition/9781803238951?utm_source=github&utm_medium=repository&utm_campaign=9781803238951) [[Amazon]](https://www.amazon.com/dp/180323895X)

* Building and Delivering Microservices on AWS [[Packt]](https://www.packtpub.com/product/building-and-delivering-microservices-on-aws/9781803238203?utm_source=github&utm_medium=repository&utm_campaign=9781803238203) [[Amazon]](https://www.amazon.com/dp/1803238208)


## Get to Know the Author
**Karen Tovmasyan**
is a Senior Software Engineer at Uber, working in the payments team and helping Uber successfully maintain its infrastructure across cloud providers. Previously he worked at various startups and consulting companies getting the most from the AWS Cloud.


## Other books by the authors
[Mastering AWS CloudFormation](https://www.packtpub.com/product/mastering-aws-cloudformation/9781789130935?utm_source=github&utm_medium=repository&utm_campaign=9781789130935)

### Download a free PDF

 <i>If you have already purchased a print or Kindle version of this book, you can get a DRM-free PDF version at no cost.<br>Simply click on the link to claim your free PDF.</i>
<p align="center"> <a href="https://packt.link/free-ebook/9781805123903">https://packt.link/free-ebook/9781805123903 </a> </p>

