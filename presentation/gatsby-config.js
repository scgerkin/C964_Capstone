/**
 * Configure your Gatsby site with this file.
 *
 * See: https://www.gatsbyjs.com/docs/gatsby-config/
 */

module.exports = {
  //todo metadata
  siteMetadata: {
    title: "C964 - CXR Prediction",
    description: "An ML app that predicts CXR diagnoses",
    author: "Stephen Gerkin",
  },
  plugins: [
    {
      resolve: `gatsby-plugin-s3`,
      options: {
        bucketName: "cxr-dx.scgrk.com"
      }
    }
    ],
}
