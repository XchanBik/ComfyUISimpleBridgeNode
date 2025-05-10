// ComfyUI.mxToolkit.Bridge v.0.1.0
import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Comfy.MxBridgeNode",
    registerCustomNodes(app) {
        // Global storage for bridges
        if (!window.mxBridgeStorage) {
            window.mxBridgeStorage = {};
        }

        // Store Bridge Node
        class MxStoreBridgeNode extends LGraphNode {
            constructor() {
                super("Store Bridge");
                this.addInput("input", "*");
                this.addOutput("output", "*");
                this.addWidget("text", "bridge_name", "bridge1", (v) => {
                    this.properties.bridge_name = v;
                });
                
                this.properties = {
                    bridge_name: "bridge1"
                };
                
                this.linkType = "*";
                this.size = this.computeSize();
                
                // Handle connection changes
                this.onConnectionsChange = function(type, index, connected, link_info) {
                    if (connected && type === LiteGraph.INPUT) {
                        const link = app.graph.links[this.inputs[0].link];
                        if (!link) return;
                        
                        const sourceNode = app.graph.getNodeById(link.origin_id);
                        const outputType = sourceNode.outputs[link.origin_slot].type || "*";
                        
                        // Update type and store
                        this.linkType = outputType;
                        this.outputs[0].type = outputType;
                        
                        // Store the connection type in the named bridge
                        window.mxBridgeStorage[this.properties.bridge_name] = {
                            type: outputType
                        };
                        
                        // Set the link color
                        const linkColor = LGraphCanvas.link_type_colors[outputType];
                        if (link) link.color = linkColor;
                    }
                    
                    // Update connections that come after this node
                    if (this.outputs && this.outputs[0] && this.outputs[0].links) {
                        for (const linkId of this.outputs[0].links) {
                            const link = app.graph.links[linkId];
                            if (!link) continue;
                            
                            link.color = LGraphCanvas.link_type_colors[this.linkType];
                        }
                    }
                };
                
                // When widget value changes
                this.onPropertyChanged = function(name, value) {
                    if (name === "bridge_name") {
                        // Register this bridge name with its type
                        if (this.linkType !== "*") {
                            window.mxBridgeStorage[value] = {
                                type: this.linkType
                            };
                        }
                    }
                };
            }
            
            // Called when node processes data
            onExecute() {
                const input = this.getInputData(0);
                if (input !== undefined) {
                    // Store the actual data
                    window.mxBridgeStorage[this.properties.bridge_name].data = input;
                    // Pass through the data
                    this.setOutputData(0, input);
                }
            }
            
            computeSize() {
                return [160, 80];
            }
        }
        
        // Load Bridge Node
        class MxLoadBridgeNode extends LGraphNode {
            constructor() {
                super("Load Bridge");
                this.addOutput("output", "*");
                this.addWidget("text", "bridge_name", "bridge1", (v) => {
                    this.properties.bridge_name = v;
                    this.updateType();
                });
                
                this.properties = {
                    bridge_name: "bridge1"
                };
                
                this.linkType = "*";
                this.size = this.computeSize();
                
                // Update type based on bridge name
                this.updateType = function() {
                    const bridgeName = this.properties.bridge_name;
                    const bridge = window.mxBridgeStorage[bridgeName];
                    
                    if (bridge && bridge.type) {
                        this.linkType = bridge.type;
                        this.outputs[0].type = bridge.type;
                        
                        // Update connection colors
                        if (this.outputs && this.outputs[0] && this.outputs[0].links) {
                            for (const linkId of this.outputs[0].links) {
                                const link = app.graph.links[linkId];
                                if (!link) continue;
                                
                                link.color = LGraphCanvas.link_type_colors[bridge.type];
                            }
                        }
                    }
                };
                
                // When property changes
                this.onPropertyChanged = function(name, value) {
                    if (name === "bridge_name") {
                        this.updateType();
                    }
                };
            }
            
            // Called when node processes data
            onExecute() {
                const bridgeName = this.properties.bridge_name;
                const bridge = window.mxBridgeStorage[bridgeName];
                
                if (bridge && bridge.data !== undefined) {
                    this.setOutputData(0, bridge.data);
                }
            }
            
            computeSize() {
                return [160, 50];
            }
        }

        // Register the nodes
        LiteGraph.registerNodeType(
            "mxStore",
            Object.assign(MxStoreBridgeNode, {
                title: "MX Store Bridge",
            })
        );
        
        LiteGraph.registerNodeType(
            "mxLoad",
            Object.assign(MxLoadBridgeNode, {
                title: "MX Load Bridge",
            })
        );
        
        MxStoreBridgeNode.category = "utils";
        MxLoadBridgeNode.category = "utils";
    },
});
