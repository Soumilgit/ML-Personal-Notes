#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ErrorCode,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  McpError,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Define the server name and version
const SERVER_NAME = "example-mcp-server";
const SERVER_VERSION = "0.1.0";

// Sample data for demonstration
const sampleData = {
  users: [
    { id: 1, name: "Alice Johnson", email: "alice@example.com", role: "admin" },
    { id: 2, name: "Bob Smith", email: "bob@example.com", role: "user" },
    { id: 3, name: "Carol Davis", email: "carol@example.com", role: "user" },
  ],
  projects: [
    { id: 1, name: "Website Redesign", status: "active", assignedTo: 1 },
    { id: 2, name: "Mobile App", status: "planning", assignedTo: 2 },
    { id: 3, name: "API Migration", status: "completed", assignedTo: 3 },
  ],
};

class ExampleMCPServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: SERVER_NAME,
        version: SERVER_VERSION,
      },
      {
        capabilities: {
          resources: {},
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    this.setupResourceHandlers();
    this.setupErrorHandling();
  }

  private setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: "get_user",
            description: "Get user information by ID",
            inputSchema: {
              type: "object",
              properties: {
                userId: {
                  type: "number",
                  description: "The user ID to retrieve",
                },
              },
              required: ["userId"],
            },
          },
          {
            name: "list_users",
            description: "List all users in the system",
            inputSchema: {
              type: "object",
              properties: {},
            },
          },
          {
            name: "create_user",
            description: "Create a new user",
            inputSchema: {
              type: "object",
              properties: {
                name: {
                  type: "string",
                  description: "User's full name",
                },
                email: {
                  type: "string",
                  description: "User's email address",
                },
                role: {
                  type: "string",
                  enum: ["admin", "user"],
                  description: "User's role",
                },
              },
              required: ["name", "email", "role"],
            },
          },
          {
            name: "get_projects",
            description: "Get projects, optionally filtered by status",
            inputSchema: {
              type: "object",
              properties: {
                status: {
                  type: "string",
                  enum: ["active", "planning", "completed"],
                  description: "Filter projects by status",
                },
              },
            },
          },
        ],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case "get_user":
            return this.handleGetUser(args as { userId: number });
          
          case "list_users":
            return this.handleListUsers();
          
          case "create_user":
            return this.handleCreateUser(args as { name: string; email: string; role: string });
          
          case "get_projects":
            return this.handleGetProjects(args as { status?: string });
          
          default:
            throw new McpError(
              ErrorCode.MethodNotFound,
              `Unknown tool: ${name}`
            );
        }
      } catch (error) {
        if (error instanceof McpError) {
          throw error;
        }
        throw new McpError(
          ErrorCode.InternalError,
          `Error executing tool ${name}: ${error}`
        );
      }
    });
  }

  private setupResourceHandlers() {
    // List available resources
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      return {
        resources: [
          {
            uri: "users://all",
            mimeType: "application/json",
            name: "All Users",
            description: "Complete list of all users in the system",
          },
          {
            uri: "projects://all",
            mimeType: "application/json", 
            name: "All Projects",
            description: "Complete list of all projects in the system",
          },
          {
            uri: "system://status",
            mimeType: "text/plain",
            name: "System Status",
            description: "Current system status and statistics",
          },
        ],
      };
    });

    // Handle resource reads
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const { uri } = request.params;

      switch (uri) {
        case "users://all":
          return {
            contents: [
              {
                uri,
                mimeType: "application/json",
                text: JSON.stringify(sampleData.users, null, 2),
              },
            ],
          };

        case "projects://all":
          return {
            contents: [
              {
                uri,
                mimeType: "application/json",
                text: JSON.stringify(sampleData.projects, null, 2),
              },
            ],
          };

        case "system://status":
          const status = {
            server: SERVER_NAME,
            version: SERVER_VERSION,
            uptime: process.uptime(),
            totalUsers: sampleData.users.length,
            totalProjects: sampleData.projects.length,
            timestamp: new Date().toISOString(),
          };
          return {
            contents: [
              {
                uri,
                mimeType: "text/plain",
                text: `System Status Report
Server: ${status.server} v${status.version}
Uptime: ${Math.floor(status.uptime)} seconds
Total Users: ${status.totalUsers}
Total Projects: ${status.totalProjects}
Generated: ${status.timestamp}`,
              },
            ],
          };

        default:
          throw new McpError(
            ErrorCode.InvalidRequest,
            `Unknown resource: ${uri}`
          );
      }
    });
  }

  private setupErrorHandling() {
    this.server.onerror = (error) => {
      console.error("[MCP Error]", error);
    };

    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  // Tool implementation methods
  private async handleGetUser(args: { userId: number }) {
    const user = sampleData.users.find(u => u.id === args.userId);
    if (!user) {
      throw new McpError(
        ErrorCode.InvalidRequest,
        `User with ID ${args.userId} not found`
      );
    }

    return {
      content: [
        {
          type: "text" as const,
          text: JSON.stringify(user, null, 2),
        },
      ],
    };
  }

  private async handleListUsers() {
    return {
      content: [
        {
          type: "text" as const,
          text: JSON.stringify(sampleData.users, null, 2),
        },
      ],
    };
  }

  private async handleCreateUser(args: { name: string; email: string; role: string }) {
    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(args.email)) {
      throw new McpError(
        ErrorCode.InvalidRequest,
        "Invalid email format"
      );
    }

    // Check if email already exists
    if (sampleData.users.some(u => u.email === args.email)) {
      throw new McpError(
        ErrorCode.InvalidRequest,
        "User with this email already exists"
      );
    }

    const newUser = {
      id: Math.max(...sampleData.users.map(u => u.id)) + 1,
      name: args.name,
      email: args.email,
      role: args.role,
    };

    sampleData.users.push(newUser);

    return {
      content: [
        {
          type: "text" as const,
          text: `User created successfully:\n${JSON.stringify(newUser, null, 2)}`,
        },
      ],
    };
  }

  private async handleGetProjects(args: { status?: string }) {
    let projects = sampleData.projects;
    
    if (args.status) {
      projects = projects.filter(p => p.status === args.status);
    }

    return {
      content: [
        {
          type: "text" as const,
          text: JSON.stringify(projects, null, 2),
        },
      ],
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error(`${SERVER_NAME} v${SERVER_VERSION} running on stdio`);
  }
}

// Start the server
const server = new ExampleMCPServer();
server.run().catch(console.error);
