# Org::Storage::Database

Manage a MySQL database on a shared RDS instance

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Org::Storage::Database",
    "Properties" : {
        "<a href="#databasename" title="DatabaseName">DatabaseName</a>" : <i>String</i>,
        "<a href="#databaseuser" title="DatabaseUser">DatabaseUser</a>" : <i>String</i>,
        "<a href="#databasepassword" title="DatabasePassword">DatabasePassword</a>" : <i>String</i>,
        "<a href="#rdshost" title="RdsHost">RdsHost</a>" : <i>String</i>,
        "<a href="#rdsuser" title="RdsUser">RdsUser</a>" : <i>String</i>,
        "<a href="#rdspassword" title="RdsPassword">RdsPassword</a>" : <i>String</i>
    }
}
</pre>

### YAML

<pre>
Type: Org::Storage::Database
Properties:
    <a href="#databasename" title="DatabaseName">DatabaseName</a>: <i>String</i>
    <a href="#databaseuser" title="DatabaseUser">DatabaseUser</a>: <i>String</i>
    <a href="#databasepassword" title="DatabasePassword">DatabasePassword</a>: <i>String</i>
    <a href="#rdshost" title="RdsHost">RdsHost</a>: <i>String</i>
    <a href="#rdsuser" title="RdsUser">RdsUser</a>: <i>String</i>
    <a href="#rdspassword" title="RdsPassword">RdsPassword</a>: <i>String</i>
</pre>

## Properties

#### DatabaseName

Database name, alphanumeric

_Required_: Yes

_Type_: String

_Pattern_: <code>^[A-Za-z0-9]+$</code>

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### DatabaseUser

Database user, alphanumeric

_Required_: Yes

_Type_: String

_Pattern_: <code>^[A-Za-z0-9]+$</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### DatabasePassword

Database password, minimum 8 symbols

_Required_: Yes

_Type_: String

_Minimum Length_: <code>8</code>

_Pattern_: <code>^[A-Za-z0-9]+$</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### RdsHost

Database endpoint

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### RdsUser

RDS admin user

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### RdsPassword

RDS admin password

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the DatabaseName.
