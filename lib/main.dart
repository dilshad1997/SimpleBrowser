import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() => runApp(SimpleBrowser());

class SimpleBrowser extends StatefulWidget {
  @override
  State<SimpleBrowser> createState() => _SimpleBrowserState();
}

class _SimpleBrowserState extends State<SimpleBrowser> {
  late WebViewController _controller;
  final TextEditingController _urlController =
      TextEditingController(text: 'https://google.com');

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Simple Browser',
      home: Scaffold(
        appBar: AppBar(
          title: TextField(
            controller: _urlController,
            decoration: InputDecoration(
              hintText: 'Enter URL (e.g. https://openai.com)',
              suffixIcon: IconButton(
                icon: Icon(Icons.search),
                onPressed: _loadUrl,
              ),
            ),
            onSubmitted: (_) => _loadUrl(),
          ),
        ),
        body: SafeArea(
          child: WebViewWidget(
            controller: _controller = WebViewController()
              ..setJavaScriptMode(JavaScriptMode.unrestricted)
              ..loadRequest(Uri.parse(_urlController.text)),
          ),
        ),
      ),
    );
  }

  void _loadUrl() {
    String url = _urlController.text.trim();
    if (!url.startsWith('http')) url = 'https://$url';
    _controller.loadRequest(Uri.parse(url));
  }
}
