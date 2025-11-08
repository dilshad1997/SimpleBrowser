import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() {
  runApp(const SimpleBrowser());
}

class SimpleBrowser extends StatelessWidget {
  const SimpleBrowser({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Simple Browser',
      debugShowCheckedModeBanner: false,
      home: const WebHome(),
    );
  }
}

class WebHome extends StatefulWidget {
  const WebHome({super.key});

  @override
  State<WebHome> createState() => _WebHomeState();
}

class _WebHomeState extends State<WebHome> {
  final controller = WebViewController();
  final TextEditingController urlController = TextEditingController(text: "https://google.com");

  @override
  void initState() {
    super.initState();
    controller
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..loadRequest(Uri.parse(urlController.text));
  }

  void _loadUrl() {
    final url = urlController.text.trim();
    if (url.isNotEmpty) {
      final uri = url.startsWith('http') ? url : 'https://$url';
      controller.loadRequest(Uri.parse(uri));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: TextField(
          controller: urlController,
          decoration: const InputDecoration(border: InputBorder.none, hintText: "Enter URL..."),
          onSubmitted: (_) => _loadUrl(),
          textInputAction: TextInputAction.go,
        ),
        actions: [
          IconButton(icon: const Icon(Icons.search), onPressed: _loadUrl),
        ],
      ),
      body: WebViewWidget(controller: controller),
    );
  }
}
