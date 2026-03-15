#!/usr/bin/env node
/**
 * Social Media MCP Server - Gold Tier Component
 * Provides Facebook, Instagram, and Twitter/X integration
 */

import axios from 'axios';
import { writeFile, readFile } from 'fs/promises';
import { join } from 'path';

class SocialMediaMCPServer {
  constructor() {
    this.config = {
      facebook: {
        accessToken: process.env.FACEBOOK_ACCESS_TOKEN,
        pageId: process.env.FACEBOOK_PAGE_ID
      },
      instagram: {
        accessToken: process.env.INSTAGRAM_ACCESS_TOKEN,
        businessAccountId: process.env.INSTAGRAM_BUSINESS_ACCOUNT_ID
      },
      twitter: {
        apiKey: process.env.TWITTER_API_KEY,
        apiSecret: process.env.TWITTER_API_SECRET,
        accessToken: process.env.TWITTER_ACCESS_TOKEN,
        accessTokenSecret: process.env.TWITTER_ACCESS_TOKEN_SECRET,
        bearerToken: process.env.TWITTER_BEARER_TOKEN
      }
    };

    this.isDryRun = process.env.DRY_RUN === 'true';
    this.vaultPath = process.env.VAULT_PATH || '/mnt/e/all-d-files/Ai_Employee_Vault';
  }

  async initialize() {
    console.log('[Social Media MCP] Server starting...');

    if (this.isDryRun) {
      console.log('[Social Media MCP] Running in DRY RUN mode');
    }

    // Validate credentials
    const hasAnyCredentials =
      this.config.facebook.accessToken ||
      this.config.instagram.accessToken ||
      this.config.twitter.bearerToken;

    if (!hasAnyCredentials && !this.isDryRun) {
      console.warn('[Social Media MCP] No API credentials configured - limited functionality');
    }

    console.log('[Social Media MCP] Server ready');
  }

  /**
   * Post to Facebook
   */
  async postToFacebook(params) {
    const { message, link, imageUrl } = params;

    if (!message) {
      throw new Error('Message is required');
    }

    if (this.isDryRun) {
      console.log('[Social Media MCP] DRY RUN - Would post to Facebook:', { message, link, imageUrl });
      return {
        success: true,
        platform: 'facebook',
        dryRun: true,
        message: 'Would post to Facebook'
      };
    }

    if (!this.config.facebook.accessToken || !this.config.facebook.pageId) {
      throw new Error('Facebook credentials not configured');
    }

    try {
      const payload = { message };
      if (link) payload.link = link;
      if (imageUrl) payload.url = imageUrl;

      const response = await axios.post(
        `https://graph.facebook.com/v18.0/${this.config.facebook.pageId}/feed`,
        payload,
        {
          params: {
            access_token: this.config.facebook.accessToken
          }
        }
      );

      return {
        success: true,
        platform: 'facebook',
        post_id: response.data.id,
        message: 'Posted to Facebook successfully'
      };

    } catch (error) {
      throw new Error(`Facebook API error: ${error.response?.data?.error?.message || error.message}`);
    }
  }

  /**
   * Post to Instagram
   */
  async postToInstagram(params) {
    const { caption, imageUrl } = params;

    if (!imageUrl) {
      throw new Error('Image URL is required for Instagram posts');
    }

    if (this.isDryRun) {
      console.log('[Social Media MCP] DRY RUN - Would post to Instagram:', { caption, imageUrl });
      return {
        success: true,
        platform: 'instagram',
        dryRun: true,
        message: 'Would post to Instagram'
      };
    }

    if (!this.config.instagram.accessToken || !this.config.instagram.businessAccountId) {
      throw new Error('Instagram credentials not configured');
    }

    try {
      // Step 1: Create media container
      const containerResponse = await axios.post(
        `https://graph.facebook.com/v18.0/${this.config.instagram.businessAccountId}/media`,
        {
          image_url: imageUrl,
          caption: caption || ''
        },
        {
          params: {
            access_token: this.config.instagram.accessToken
          }
        }
      );

      const containerId = containerResponse.data.id;

      // Step 2: Publish media
      const publishResponse = await axios.post(
        `https://graph.facebook.com/v18.0/${this.config.instagram.businessAccountId}/media_publish`,
        {
          creation_id: containerId
        },
        {
          params: {
            access_token: this.config.instagram.accessToken
          }
        }
      );

      return {
        success: true,
        platform: 'instagram',
        post_id: publishResponse.data.id,
        message: 'Posted to Instagram successfully'
      };

    } catch (error) {
      throw new Error(`Instagram API error: ${error.response?.data?.error?.message || error.message}`);
    }
  }

  /**
   * Post to Twitter/X
   */
  async postToTwitter(params) {
    const { text, mediaIds } = params;

    if (!text) {
      throw new Error('Text is required');
    }

    if (text.length > 280) {
      throw new Error('Tweet text exceeds 280 characters');
    }

    if (this.isDryRun) {
      console.log('[Social Media MCP] DRY RUN - Would post to Twitter:', { text, mediaIds });
      return {
        success: true,
        platform: 'twitter',
        dryRun: true,
        message: 'Would post to Twitter'
      };
    }

    if (!this.config.twitter.bearerToken) {
      throw new Error('Twitter credentials not configured');
    }

    try {
      const payload = { text };
      if (mediaIds && mediaIds.length > 0) {
        payload.media = { media_ids: mediaIds };
      }

      const response = await axios.post(
        'https://api.twitter.com/2/tweets',
        payload,
        {
          headers: {
            'Authorization': `Bearer ${this.config.twitter.bearerToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      return {
        success: true,
        platform: 'twitter',
        tweet_id: response.data.data.id,
        message: 'Posted to Twitter successfully'
      };

    } catch (error) {
      throw new Error(`Twitter API error: ${error.response?.data?.detail || error.message}`);
    }
  }

  /**
   * Cross-post to multiple platforms
   */
  async crossPost(params) {
    const { platforms, content } = params;

    if (!platforms || platforms.length === 0) {
      throw new Error('At least one platform must be specified');
    }

    const results = [];
    const errors = [];

    for (const platform of platforms) {
      try {
        let result;

        switch (platform.toLowerCase()) {
          case 'facebook':
            result = await this.postToFacebook({
              message: content.text,
              link: content.link,
              imageUrl: content.imageUrl
            });
            break;

          case 'instagram':
            if (!content.imageUrl) {
              throw new Error('Image required for Instagram');
            }
            result = await this.postToInstagram({
              caption: content.text,
              imageUrl: content.imageUrl
            });
            break;

          case 'twitter':
          case 'x':
            result = await this.postToTwitter({
              text: content.text.substring(0, 280),
              mediaIds: content.mediaIds
            });
            break;

          default:
            throw new Error(`Unknown platform: ${platform}`);
        }

        results.push(result);

      } catch (error) {
        errors.push({
          platform,
          error: error.message
        });
      }
    }

    return {
      success: errors.length === 0,
      results,
      errors: errors.length > 0 ? errors : undefined,
      summary: `Posted to ${results.length} of ${platforms.length} platforms`
    };
  }

  /**
   * Generate social media summary from recent posts
   */
  async generateSummary(params) {
    const { platform, limit = 10 } = params;

    if (this.isDryRun) {
      console.log('[Social Media MCP] DRY RUN - Would fetch posts from:', platform);
      return {
        success: true,
        dryRun: true,
        summary: 'Dry run mode - no actual data fetched'
      };
    }

    try {
      let posts = [];

      switch (platform.toLowerCase()) {
        case 'facebook':
          posts = await this._fetchFacebookPosts(limit);
          break;

        case 'instagram':
          posts = await this._fetchInstagramPosts(limit);
          break;

        case 'twitter':
        case 'x':
          posts = await this._fetchTwitterPosts(limit);
          break;

        default:
          throw new Error(`Unknown platform: ${platform}`);
      }

      // Generate summary
      const summary = {
        platform,
        total_posts: posts.length,
        posts: posts.map(p => ({
          id: p.id,
          text: p.text || p.message || p.caption || '',
          created_at: p.created_time || p.timestamp || p.created_at,
          engagement: p.likes + p.comments + (p.shares || 0)
        })),
        total_engagement: posts.reduce((sum, p) => sum + p.likes + p.comments + (p.shares || 0), 0)
      };

      return {
        success: true,
        summary
      };

    } catch (error) {
      throw new Error(`Error generating summary: ${error.message}`);
    }
  }

  async _fetchFacebookPosts(limit) {
    if (!this.config.facebook.accessToken || !this.config.facebook.pageId) {
      throw new Error('Facebook credentials not configured');
    }

    const response = await axios.get(
      `https://graph.facebook.com/v18.0/${this.config.facebook.pageId}/posts`,
      {
        params: {
          access_token: this.config.facebook.accessToken,
          fields: 'id,message,created_time,likes.summary(true),comments.summary(true),shares',
          limit
        }
      }
    );

    return response.data.data.map(post => ({
      id: post.id,
      message: post.message,
      created_time: post.created_time,
      likes: post.likes?.summary?.total_count || 0,
      comments: post.comments?.summary?.total_count || 0,
      shares: post.shares?.count || 0
    }));
  }

  async _fetchInstagramPosts(limit) {
    if (!this.config.instagram.accessToken || !this.config.instagram.businessAccountId) {
      throw new Error('Instagram credentials not configured');
    }

    const response = await axios.get(
      `https://graph.facebook.com/v18.0/${this.config.instagram.businessAccountId}/media`,
      {
        params: {
          access_token: this.config.instagram.accessToken,
          fields: 'id,caption,timestamp,like_count,comments_count',
          limit
        }
      }
    );

    return response.data.data.map(post => ({
      id: post.id,
      caption: post.caption,
      timestamp: post.timestamp,
      likes: post.like_count || 0,
      comments: post.comments_count || 0,
      shares: 0
    }));
  }

  async _fetchTwitterPosts(limit) {
    if (!this.config.twitter.bearerToken) {
      throw new Error('Twitter credentials not configured');
    }

    // Note: This requires Twitter API v2 with elevated access
    const response = await axios.get(
      'https://api.twitter.com/2/tweets/search/recent',
      {
        params: {
          query: 'from:me',
          max_results: limit,
          'tweet.fields': 'created_at,public_metrics'
        },
        headers: {
          'Authorization': `Bearer ${this.config.twitter.bearerToken}`
        }
      }
    );

    return (response.data.data || []).map(tweet => ({
      id: tweet.id,
      text: tweet.text,
      created_at: tweet.created_at,
      likes: tweet.public_metrics?.like_count || 0,
      comments: tweet.public_metrics?.reply_count || 0,
      shares: tweet.public_metrics?.retweet_count || 0
    }));
  }

  /**
   * MCP Protocol: List available tools
   */
  listTools() {
    return [
      {
        name: 'post_to_facebook',
        description: 'Post a message to Facebook page',
        inputSchema: {
          type: 'object',
          properties: {
            message: { type: 'string', description: 'Post text', required: true },
            link: { type: 'string', description: 'Optional link to share' },
            imageUrl: { type: 'string', description: 'Optional image URL' }
          },
          required: ['message']
        }
      },
      {
        name: 'post_to_instagram',
        description: 'Post an image to Instagram',
        inputSchema: {
          type: 'object',
          properties: {
            imageUrl: { type: 'string', description: 'Image URL (required)', required: true },
            caption: { type: 'string', description: 'Post caption' }
          },
          required: ['imageUrl']
        }
      },
      {
        name: 'post_to_twitter',
        description: 'Post a tweet to Twitter/X',
        inputSchema: {
          type: 'object',
          properties: {
            text: { type: 'string', description: 'Tweet text (max 280 chars)', required: true },
            mediaIds: {
              type: 'array',
              description: 'Optional media IDs',
              items: { type: 'string' }
            }
          },
          required: ['text']
        }
      },
      {
        name: 'cross_post',
        description: 'Post the same content to multiple platforms',
        inputSchema: {
          type: 'object',
          properties: {
            platforms: {
              type: 'array',
              description: 'Platforms to post to',
              items: { type: 'string', enum: ['facebook', 'instagram', 'twitter', 'x'] },
              required: true
            },
            content: {
              type: 'object',
              description: 'Content to post',
              properties: {
                text: { type: 'string' },
                imageUrl: { type: 'string' },
                link: { type: 'string' },
                mediaIds: { type: 'array', items: { type: 'string' } }
              },
              required: true
            }
          },
          required: ['platforms', 'content']
        }
      },
      {
        name: 'generate_summary',
        description: 'Generate summary from recent posts on a platform',
        inputSchema: {
          type: 'object',
          properties: {
            platform: {
              type: 'string',
              description: 'Platform to summarize',
              enum: ['facebook', 'instagram', 'twitter', 'x'],
              required: true
            },
            limit: { type: 'number', description: 'Number of recent posts to analyze (default: 10)' }
          },
          required: ['platform']
        }
      }
    ];
  }

  /**
   * MCP Protocol: Execute a tool
   */
  async executeTool(toolName, params) {
    switch (toolName) {
      case 'post_to_facebook':
        return await this.postToFacebook(params);

      case 'post_to_instagram':
        return await this.postToInstagram(params);

      case 'post_to_twitter':
        return await this.postToTwitter(params);

      case 'cross_post':
        return await this.crossPost(params);

      case 'generate_summary':
        return await this.generateSummary(params);

      default:
        throw new Error(`Unknown tool: ${toolName}`);
    }
  }

  /**
   * Start MCP server (stdio mode)
   */
  async start() {
    await this.initialize();

    console.log('[Social Media MCP] Available tools:', this.listTools().map(t => t.name).join(', '));
    console.log('[Social Media MCP] Listening on stdin...');

    // MCP stdio protocol implementation
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', async (data) => {
      try {
        const request = JSON.parse(data);
        let response;

        switch (request.method) {
          case 'tools/list':
            response = { tools: this.listTools() };
            break;

          case 'tools/call':
            const result = await this.executeTool(request.params.name, request.params.arguments || {});
            response = { content: [{ type: 'text', text: JSON.stringify(result) }] };
            break;

          default:
            throw new Error(`Unknown method: ${request.method}`);
        }

        process.stdout.write(JSON.stringify({ id: request.id, result: response }) + '\n');

      } catch (error) {
        process.stdout.write(JSON.stringify({
          id: request?.id,
          error: { message: error.message }
        }) + '\n');
      }
    });
  }
}

// Start server
const server = new SocialMediaMCPServer();
server.start().catch(error => {
  console.error('[Social Media MCP] Fatal error:', error);
  process.exit(1);
});
