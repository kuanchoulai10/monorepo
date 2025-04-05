resource "aws_iam_policy" "bigquery_omni_connection_policy" {
  name = "bigquery-omni-connection-policy"

  policy = <<-EOF
            {
              "Version": "2012-10-17",
              "Statement": [
                  {
                      "Sid": "BucketLevelAccess",
                      "Effect": "Allow",
                      "Action": ["s3:ListBucket"],
                      "Resource": ["arn:aws:s3:::kcl-bigquery"]
                  },
                  {
                      "Sid": "ObjectLevelAccess",
                      "Effect": "Allow",
                      "Action": ["s3:GetObject","s3:PutObject"],
                      "Resource": [
                          "arn:aws:s3:::kcl-bigquery",
                          "arn:aws:s3:::kcl-bigquery/*"
                          ]
                  }
              ]
            }
            EOF
}

resource "aws_iam_role" "bigquery_omni_connection_role" {
  name                 = "bigquery-omni-connection"
  max_session_duration = 43200

  assume_role_policy = <<-EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Federated": "accounts.google.com"
          },
          "Action": "sts:AssumeRoleWithWebIdentity",
          "Condition": {
            "StringEquals": {
              "accounts.google.com:sub": "${google_bigquery_connection.connection.aws[0].access_role[0].identity}"
            }
          }
        }
      ]
    }
    EOF
}

resource "aws_iam_role_policy_attachment" "bigquery_omni_connection_role_attach" {
  role       = aws_iam_role.bigquery_omni_connection_role.name
  policy_arn = aws_iam_policy.bigquery_omni_connection_policy.arn
}

resource "google_bigquery_connection" "connection" {
  connection_id = "bigquery-omni-aws-connection"
  friendly_name = "bigquery-omni-aws-connection"
  description   = "Created by Terraform"

  location = "aws-us-west-2"
  aws {
    access_role {
      # This must be constructed as a string instead of referencing the
      # AWS resources directly to avoid a resource dependency cycle
      # in Terraform.
      iam_role_id = "arn:aws:iam::545757050262:role/bigquery-omni-connection"
    }
  }
}
