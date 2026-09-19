const vscode = require('vscode');
const { LanguageClient, TransportKind } = require('vscode-languageclient/node');

let client;

/**
 * Activates the Hinglish language client extension.
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    const config = vscode.workspace.getConfiguration('hinglish');
    const enabled = config.get('lsp.enabled', true);

    if (!enabled) {
        return;
    }

    const customPath = config.get('lsp.path', 'hinglish-lsp');
    const pythonPath = config.get('lsp.pythonPath', 'python3');

    // Configure language server execution options
    const serverOptions = {
        run: {
            command: customPath,
            args: [],
            options: { shell: true },
            transport: TransportKind.stdio
        },
        debug: {
            command: pythonPath,
            args: ['-m', 'hinglish.lsp'],
            options: { shell: true },
            transport: TransportKind.stdio
        }
    };

    // Options to control the language client
    const clientOptions = {
        documentSelector: [{ scheme: 'file', language: 'hinglish' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.hin')
        }
    };

    // Create the language client and start the client
    client = new LanguageClient(
        'hinglishLsp',
        'Hinglish Language Server',
        serverOptions,
        clientOptions
    );

    client.start().catch((err) => {
        // If the primary command fails, attempt fallback using python interpreter
        const fallbackServerOptions = {
            command: pythonPath,
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
