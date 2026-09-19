const vscode = require('vscode');
const { LanguageClient, TransportKind } = require('vscode-languageclient/node');

let client;

/**
 * Activates the Hinglish language client and debug adapter extensions.
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    // -------------------------------------------------------------------------
    // 1. Language Server Protocol (LSP) Client
    // -------------------------------------------------------------------------
    const config = vscode.workspace.getConfiguration('hinglish');
    const lspEnabled = config.get('lsp.enabled', true);

    if (lspEnabled) {
        const lspCustomPath = config.get('lsp.path', 'hinglish-lsp');
        const lspPythonPath = config.get('lsp.pythonPath', 'python3');

        const serverOptions = {
            run: {
                command: lspCustomPath,
                args: [],
                options: { shell: true },
                transport: TransportKind.stdio
            },
            debug: {
                command: lspPythonPath,
                args: ['-m', 'hinglish.lsp'],
                options: { shell: true },
                transport: TransportKind.stdio
            }
        };

        const clientOptions = {
            documentSelector: [{ scheme: 'file', language: 'hinglish' }],
            synchronize: {
                fileEvents: vscode.workspace.createFileSystemWatcher('**/*.hin')
            }
        };

        client = new LanguageClient(
            'hinglishLsp',
            'Hinglish Language Server',
            serverOptions,
            clientOptions
        );

        client.start().catch((err) => {
            const fallbackServerOptions = {
                command: lspPythonPath,
                args: ['-m', 'hinglish.lsp'],
                options: { shell: true },
                transport: TransportKind.stdio
            };

            client = new LanguageClient(
                'hinglishLspFallback',
                'Hinglish Language Server',
                fallbackServerOptions,
                clientOptions
            );

            client.start().catch((fallbackErr) => {
                vscode.window.showWarningMessage(
                    `Hinglish Language Server is not running (${fallbackErr.message}). Install Hinglish using "pip install ." to enable diagnostics and autocompletion.`
                );
            });
        });
    }

    // -------------------------------------------------------------------------
    // 2. Debug Adapter Protocol (DAP) Integration
    // -------------------------------------------------------------------------
    const provider = new HinglishConfigurationProvider();
    context.subscriptions.push(
        vscode.debug.registerDebugConfigurationProvider('hinglish', provider)
    );

    const factory = new HinglishDebugAdapterDescriptorFactory();
    context.subscriptions.push(
        vscode.debug.registerDebugAdapterDescriptorFactory('hinglish', factory)
    );
}

/**
 * Provides default debug configuration when user presses F5.
 */
class HinglishConfigurationProvider {
    resolveDebugConfiguration(folder, config, token) {
        if (!config.type && !config.request && !config.name) {
            const editor = vscode.window.activeTextEditor;
            if (editor && editor.document.languageId === 'hinglish') {
                config.type = 'hinglish';
                config.name = 'Launch Hinglish Program';
                config.request = 'launch';
                config.program = '${file}';
                config.stopOnEntry = false;
            }
        }

        if (!config.program) {
            return vscode.window.showInformationMessage('Cannot find a Hinglish .hin file to debug.').then(() => {
                return undefined;
            });
        }

        return config;
    }
}

/**
 * Creates Debug Adapter Executable pointing to hinglish-dap or python -m hinglish.dap.
 */
class HinglishDebugAdapterDescriptorFactory {
    createDebugAdapterDescriptor(session, executable) {
        const config = vscode.workspace.getConfiguration('hinglish');
        const dapCustomPath = config.get('dap.path', 'hinglish-dap');
        const dapPythonPath = config.get('dap.pythonPath', 'python3');

        // Prefer hinglish-dap executable, fallback to python3 -m hinglish.dap
        return new vscode.DebugAdapterExecutable(
            dapCustomPath,
            [],
            {
                shell: true,
                env: process.env
            }
        );
    }
}

/**
 * Deactivates the extension and stops the language client.
 */
function deactivate() {
    if (!client) {
        return undefined;
    }
    return client.stop();
}

module.exports = {
    activate,
    deactivate
};
